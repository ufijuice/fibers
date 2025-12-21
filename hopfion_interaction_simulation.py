import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from skimage.measure import marching_cubes
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.colors as colors
from scipy.ndimage import map_coordinates, center_of_mass
import click
import os
import time

# --- Core Simulation & Analysis Logic ---

def run_vnlse_simulation(initial_field_x, initial_field_y, dx, dy, d_z_grid, dz, num_steps, k, k0, n2, store_interval=10):
    """
    Solves the 3D Vector NLSE using a symmetric split-step Fourier method.
    """
    nx, ny, nz = initial_field_x.shape
    kx, ky, kz = (2 * np.pi * np.fft.fftfreq(n, d=d) for n, d in zip((nx, ny, nz), (dx, dy, d_z_grid)))
    KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing='ij')
    linear_operator = np.exp(-1j * (KX**2 + KY**2 + KZ**2) / (2 * k) * dz / 2)
    field_x, field_y = initial_field_x.copy(), initial_field_y.copy()
    gamma = k0 * n2
    stored_fields = []
    click.echo("Running VNLSE simulation...")
    for i in range(num_steps):
        # --- First half linear step ---
        field_x_k = np.fft.fftn(field_x) * linear_operator
        field_x = np.fft.ifftn(field_x_k)
        field_y_k = np.fft.fftn(field_y) * linear_operator
        field_y = np.fft.ifftn(field_y_k)

        # --- Full nonlinear step ---
        abs_field_x_sq, abs_field_y_sq = np.abs(field_x)**2, np.abs(field_y)**2
        angle_x, angle_y = np.angle(field_x), np.angle(field_y)
        nonlinear_phase_x = np.exp(1j * gamma * (abs_field_x_sq + (2/3)*abs_field_y_sq + (1/3)*abs_field_y_sq*np.cos(2*angle_y - 2*angle_x)) * dz)
        nonlinear_phase_y = np.exp(1j * gamma * (abs_field_y_sq + (2/3)*abs_field_x_sq + (1/3)*abs_field_x_sq*np.cos(2*angle_x - 2*angle_y)) * dz)
        field_x *= nonlinear_phase_x
        field_y *= nonlinear_phase_y

        # --- Second half linear step ---
        field_x_k = np.fft.fftn(field_x) * linear_operator
        field_x = np.fft.ifftn(field_x_k)
        field_y_k = np.fft.fftn(field_y) * linear_operator
        field_y = np.fft.ifftn(field_y_k)
        
        if (i + 1) % store_interval == 0:
            stored_fields.append((field_x.copy(), field_y.copy()))
            click.echo(f"Step {i+1}/{num_steps} completed. Storing fields.")
    return stored_fields

def create_single_hopfion(grid, power, R_hopfion, sigma, center, velocity, phase):
    X, Y, Z = grid
    x0, y0, z0 = center
    vx, vy = velocity
    X_shifted, Y_shifted, Z_shifted = X - x0, Y - y0, Z - z0
    u, v = X_shifted + 1j * Y_shifted, Z_shifted + 1j * R_hopfion
    psi1_raw, psi2_raw = u + 1j * v, v + 1j * np.conj(u)
    norm = np.sqrt(np.abs(psi1_raw)**2 + np.abs(psi2_raw)**2)
    norm[norm < 1e-9] = 1e-9
    amp = np.exp(-(X_shifted**2 + Y_shifted**2 + Z_shifted**2) / (2 * sigma**2))
    field_x = np.sqrt(power) * (psi1_raw / norm) * amp * np.exp(1j * (vx*X_shifted + vy*Y_shifted + phase))
    field_y = np.sqrt(power) * (psi2_raw / norm) * amp * np.exp(1j * (vx*X_shifted + vy*Y_shifted + phase))
    return field_x, field_y

def create_two_hopfions_initial_field(sim_params):
    x, y, z = (np.linspace(-sim_params['sim_size'], sim_params['sim_size'], sim_params['grid_size']) for _ in range(3))
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    grid = (X, Y, Z)
    dx, dy, d_z_grid = x[1] - x[0], y[1] - y[0], z[1] - z[0]
    h1_x, h1_y = create_single_hopfion(grid, sim_params['power'], sim_params['R_hopfion'], sim_params['sigma'], sim_params['center1'], sim_params['velocity1'], sim_params['phase1'])
    h2_x, h2_y = create_single_hopfion(grid, sim_params['power'], sim_params['R_hopfion'], sim_params['sigma'], sim_params['center2'], sim_params['velocity2'], sim_params['phase2'])
    return h1_x + h2_x, h1_y + h2_y, dx, dy, d_z_grid

def find_hopfion_centers(intensity, grid_size):
    mid_point = grid_size // 2
    left_half, right_half = intensity.copy(), intensity.copy()
    left_half[mid_point:, :, :] = 0
    right_half[:mid_point, :, :] = 0
    return np.array(center_of_mass(left_half)), np.array(center_of_mass(right_half))

# --- Visualization ---
def animate_3d_time_evolution(stored_fields, sim_params, filename):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    cmap, norm = plt.get_cmap('coolwarm'), colors.Normalize(vmin=-1, vmax=1)
    isolevel_fraction = 0.4

    def update(frame):
        ax.clear()
        field_x, field_y = stored_fields[frame]
        total_intensity = np.abs(field_x)**2 + np.abs(field_y)**2
        s3_normalized = (2 * np.imag(np.conj(field_x) * field_y)) / (total_intensity + 1e-11)
        isolevel = total_intensity.max() * isolevel_fraction
        try:
            verts, faces, _, _ = marching_cubes(np.pad(total_intensity, 1), level=isolevel)
            verts -= 1
            verts_scaled = -sim_params['sim_size'] + verts * (2 * sim_params['sim_size'] / (sim_params['grid_size'] - 1))
        except (ValueError, RuntimeError):
            click.echo(f"Frame {frame}: Marching cubes failed.", err=True); return []
        s3_values = map_coordinates(np.pad(s3_normalized, 1).astype(np.float64), verts.T, order=1)
        face_colors = cmap(norm(s3_values[faces].mean(axis=1)))
        mesh = Poly3DCollection(verts_scaled[:, [2, 1, 0]][faces], facecolors=face_colors, edgecolor='k', linewidth=0.1, alpha=0.9)
        ax.add_collection3d(mesh)
        ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
        ax.set_xlim(-sim_params['sim_size'], sim_params['sim_size']); ax.set_ylim(-sim_params['sim_size'], sim_params['sim_size']); ax.set_zlim(-sim_params['sim_size'], sim_params['sim_size'])
        ax.set_title(f"3D Interaction, Step {frame * sim_params['store_interval']}")
        click.echo(f"Rendering time-evolution frame {frame+1}/{len(stored_fields)}")
        return [mesh]

    anim = animation.FuncAnimation(fig, update, frames=len(stored_fields), blit=False)
    click.echo(f"Saving 3D time-evolution animation to {filename}..."); anim.save(filename, writer='pillow', fps=5, dpi=100); click.echo("Saved."); plt.close(fig)

def animate_3d_turntable(fields, sim_params, filename):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    cmap, norm = plt.get_cmap('coolwarm'), colors.Normalize(vmin=-1, vmax=1)
    field_x, field_y = fields
    total_intensity = np.abs(field_x)**2 + np.abs(field_y)**2
    s3_normalized = (2 * np.imag(np.conj(field_x) * field_y)) / (total_intensity + 1e-11)
    isolevel = total_intensity.max() * 0.4
    try:
        verts, faces, _, _ = marching_cubes(np.pad(total_intensity, 1), level=isolevel)
        verts -= 1
        verts_scaled = -sim_params['sim_size'] + verts * (2 * sim_params['sim_size'] / (sim_params['grid_size'] - 1))
    except (ValueError, RuntimeError):
        click.echo("Turntable: Marching cubes failed.", err=True); plt.close(fig); return
    s3_values = map_coordinates(np.pad(s3_normalized, 1).astype(np.float64), verts.T, order=1)
    face_colors = cmap(norm(s3_values[faces].mean(axis=1)))
    mesh = Poly3DCollection(verts_scaled[:, [2, 1, 0]][faces], facecolors=face_colors, edgecolor='k', linewidth=0.1, alpha=0.9)
    ax.add_collection3d(mesh)
    ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
    ax.set_xlim(-sim_params['sim_size'], sim_params['sim_size']); ax.set_ylim(-sim_params['sim_size'], sim_params['sim_size']); ax.set_zlim(-sim_params['sim_size'], sim_params['sim_size'])
    fig.colorbar(plt.cm.ScalarMappable(cmap=cmap, norm=norm), ax=ax, shrink=0.6).set_label('Normalized S3 Parameter')
    anim = animation.FuncAnimation(fig, lambda a: (ax.view_init(elev=30, azim=a), ax.set_title(f"3D Turntable (Angle: {a:.1f}°)"), click.echo(f"Rendering angle {a:.1f}°")), frames=np.linspace(0, 360, 90), blit=False)
    click.echo(f"Saving turntable animation to {filename}..."); anim.save(filename, writer='pillow', fps=15, dpi=100); click.echo("Saved."); plt.close(fig)

# --- CLI command definitions ---
def common_run_options(func):
    options = [
        click.option('--grid-size', default=64, type=int, help='Grid size for the simulation box.'),
        click.option('--sim-size', default=10.0, type=float, help='Spatial size of the simulation box (e.g., from -10 to 10).'),
        click.option('--power', default=6.87e3, type=float, help='Optical power of the hopfions.'),
        click.option('--num-steps', default=350, type=int, help='Number of propagation steps.'),
        click.option('--store-interval', default=10, type=int, help='Interval to store frames for animations.'),
        click.option('--velocity', default=5.0, type=float, help='Initial transverse velocity of the hopfions.'),
        click.option('--separation', default=10.0, type=float, help='Initial separation on the x-axis.'),
        click.option('--phase1', default=0.0, type=float, help='Initial phase of the first hopfion (in radians).'),
        click.option('--phase2', default=np.pi, type=float, help='Initial phase of the second hopfion (in radians).'),
        click.option('--output-dir', default='results', type=click.Path(), help='Directory to save results.')
    ]
    for option in reversed(options): func = option(func)
    return func

def _run_simulation(sim_params, output_dir):
    initial_field_x, initial_field_y, dx, dy, d_z_grid = create_two_hopfions_initial_field(sim_params)
    k0 = 2 * np.pi / sim_params['wavelength']; k = k0 * sim_params['n0_algaas']
    stored_fields = run_vnlse_simulation(initial_field_x, initial_field_y, dx, dy, d_z_grid, sim_params['dz'], sim_params['num_steps'], k, k0, sim_params['n2_algaas'], store_interval=sim_params['store_interval'])
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"hopfion_interaction_{time.strftime('%Y%m%d-%H%M%S')}.npz")
    click.echo(f"Saving results to {filepath}..."); np.savez_compressed(filepath, stored_fields=np.array(stored_fields, dtype=object), sim_params=sim_params); click.echo("Saved.")
    return filepath, stored_fields

def _analyze_results(result_file, stored_fields, sim_params):
    click.echo("\n--- Analyzing Frames (coordinates are in grid units) ---")
    distances = []
    for i, (field_x, field_y) in enumerate(stored_fields):
        total_intensity = np.abs(field_x)**2 + np.abs(field_y)**2
        center1, center2 = find_hopfion_centers(total_intensity, sim_params['grid_size'])
        distance = np.linalg.norm(center1 - center2)
        distances.append(distance)
        click.echo(f"Frame {i}: Center 1: ({center1[0]:.1f}, {center1[1]:.1f}, {center1[2]:.1f}), Center 2: ({center2[0]:.1f}, {center2[1]:.1f}, {center2[2]:.1f}), Distance = {distance:.2f}")
    if not distances:
        click.echo("No frames to analyze.", err=True); return None
    min_dist_frame = np.argmin(distances)
    click.echo("\n--- Analysis Complete ---")
    click.echo(f"Peak interaction found at frame: {min_dist_frame}")
    click.echo(f"Minimum distance: {distances[min_dist_frame]:.2f} grid units")
    return min_dist_frame

@click.group()
def cli(): """A CLI for simulating and visualizing Hopfion interactions."""

@cli.command()
@common_run_options
def run(**kwargs):
    """Runs the simulation and saves the results."""
    sim_params = {**kwargs, 'R_hopfion': 1.0, 'sigma': 1.0, 'wavelength': 1.55, 'n0_algaas': 3.3, 'n2_algaas': 1e-5, 'dz': 0.1}
    sim_params.update({'center1': (-kwargs['separation']/2,0,0), 'velocity1': (kwargs['velocity'],0), 'center2': (kwargs['separation']/2,0,0), 'velocity2': (-kwargs['velocity'],0)})
    _run_simulation(sim_params, kwargs['output_dir'])

@cli.command()
@common_run_options
def run_and_visualize(**kwargs):
    """Run simulation, save, and create a 3D time-evolution animation."""
    sim_params = {**kwargs, 'R_hopfion': 1.0, 'sigma': 1.0, 'wavelength': 1.55, 'n0_algaas': 3.3, 'n2_algaas': 1e-5, 'dz': 0.1}
    sim_params.update({'center1': (-kwargs['separation']/2,0,0), 'velocity1': (kwargs['velocity'],0), 'center2': (kwargs['separation']/2,0,0), 'velocity2': (-kwargs['velocity'],0)})
    _, stored_fields = _run_simulation(sim_params, kwargs['output_dir'])
    output_filename = f"time_evolution_{time.strftime('%Y%m%d-%H%M%S')}.gif"
    click.echo(f"\nCreating 3D time-evolution animation...")
    animate_3d_time_evolution(stored_fields, sim_params, filename=output_filename)

@cli.command()
@click.argument('result_file', type=click.Path(exists=True))
def analyze(result_file):
    """Analyzes a result file to find the peak interaction frame."""
    data = np.load(result_file, allow_pickle=True)
    peak_frame = _analyze_results(result_file, data['stored_fields'], data['sim_params'].item())
    click.echo("\nUse this frame number to create a detailed visualization:")
    click.echo(f"python3 hopfion_interaction_simulation.py visualize turntable --frame {peak_frame} {result_file}")

@cli.group()
def visualize(): """Visualization commands."""

@visualize.command(name='turntable')
@click.argument('result_file', type=click.Path(exists=True))
@click.option('--frame', default=-1, type=int, help='Frame to visualize (-1 for last frame).')
def visualize_turntable(result_file, frame):
    """Creates a 3D turntable animation from a result file."""
    data = np.load(result_file, allow_pickle=True)
    if not data['stored_fields'].any() or abs(frame) > len(data['stored_fields']):
        click.echo(f"Invalid frame. File has {len(data['stored_fields'])} frames.", err=True); return
    output_filename = f"turntable_frame{frame}_{os.path.basename(result_file).replace('.npz', '.gif')}"
    click.echo(f"\nCreating turntable for frame {frame} of {os.path.basename(result_file)}...")
    animate_3d_turntable(data['stored_fields'][frame], data['sim_params'].item(), filename=output_filename)

if __name__ == '__main__':
    cli()