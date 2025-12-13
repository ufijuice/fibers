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

# --- Core Simulation Function ---
def run_vnlse_simulation(initial_field_x, initial_field_y, dx, dy, dz, num_steps, k, k0, n2, store_interval=10):
    nx, ny, nz = initial_field_x.shape
    kx = 2 * np.pi * np.fft.fftfreq(nx, d=dx)
    ky = 2 * np.pi * np.fft.fftfreq(ny, d=dy)
    KX, KY = np.meshgrid(kx, ky)
    linear_operator = np.exp(-1j * (KX**2 + KY**2) / (2 * k) * dz / 2)

    field_x, field_y = initial_field_x.copy(), initial_field_y.copy()
    gamma = k0 * n2
    stored_fields = []

    print("Running VNLSE simulation...")
    for i in range(num_steps):
        field_x_k = np.fft.fft2(field_x, axes=(0, 1)) * linear_operator
        field_x = np.fft.ifft2(field_x_k, axes=(0, 1))
        field_y_k = np.fft.fft2(field_y, axes=(0, 1)) * linear_operator
        field_y = np.fft.ifft2(field_y_k, axes=(0, 1))

        abs_field_x_sq = np.abs(field_x)**2
        abs_field_y_sq = np.abs(field_y)**2
        nonlinear_phase_x = np.exp(1j * gamma * (abs_field_x_sq + (2/3) * abs_field_y_sq + (1/3) * np.abs(field_y)**2 * np.cos(2 * np.angle(field_y) - 2 * np.angle(field_x))) * dz)
        nonlinear_phase_y = np.exp(1j * gamma * (abs_field_y_sq + (2/3) * abs_field_x_sq + (1/3) * np.abs(field_x)**2 * np.cos(2 * np.angle(field_x) - 2 * np.angle(field_y))) * dz)
        field_x *= nonlinear_phase_x
        field_y *= nonlinear_phase_y

        field_x_k = np.fft.fft2(field_x, axes=(0, 1)) * linear_operator
        field_x = np.fft.ifft2(field_x_k, axes=(0, 1))
        field_y_k = np.fft.fft2(field_y, axes=(0, 1)) * linear_operator
        field_y = np.fft.ifft2(field_y_k, axes=(0, 1))
        
        if (i + 1) % store_interval == 0:
            stored_fields.append((field_x.copy(), field_y.copy()))
            click.echo(f"Step {i+1}/{num_steps} completed. Storing fields.")
    return stored_fields

# --- Initial Field Creation ---
def create_single_hopfion(grid, power, R_hopfion, sigma, center, velocity, phase):
    X, Y, Z = grid
    x0, y0, z0 = center
    vx, vy = velocity
    X_shifted, Y_shifted, Z_shifted = X - x0, Y - y0, Z - z0

    u = X_shifted + 1j * Y_shifted
    v = Z_shifted + 1j * R_hopfion
    psi1_raw = u + 1j * v
    psi2_raw = v + 1j * np.conj(u)

    total_intensity_norm = np.sqrt(np.abs(psi1_raw)**2 + np.abs(psi2_raw)**2)
    total_intensity_norm[total_intensity_norm < 1e-9] = 1e-9
    
    amplitude_profile = np.exp(-(X_shifted**2 + Y_shifted**2 + Z_shifted**2) / (2 * sigma**2))
    field_x = np.sqrt(power) * (psi1_raw / total_intensity_norm) * amplitude_profile
    field_y = np.sqrt(power) * (psi2_raw / total_intensity_norm) * amplitude_profile

    phase_ramp = np.exp(1j * (vx * X_shifted + vy * Y_shifted))
    phase_shift = np.exp(1j * phase)
    field_x *= phase_ramp * phase_shift
    field_y *= phase_ramp * phase_shift
    return field_x, field_y

def create_two_hopfions_initial_field(sim_params):
    x = np.linspace(-sim_params['sim_size'], sim_params['sim_size'], sim_params['grid_size'])
    y = np.linspace(-sim_params['sim_size'], sim_params['sim_size'], sim_params['grid_size'])
    z = np.linspace(-sim_params['sim_size'], sim_params['sim_size'], sim_params['grid_size'])
    X, Y, Z = np.meshgrid(x, y, z)
    grid = (X, Y, Z)
    dx = x[1] - x[0]
    dy = y[1] - y[0]

    hopfion1_x, hopfion1_y = create_single_hopfion(grid, sim_params['power'], sim_params['r_hopfion'], sim_params['sigma'], sim_params['center1'], sim_params['velocity1'], sim_params['phase1'])
    hopfion2_x, hopfion2_y = create_single_hopfion(grid, sim_params['power'], sim_params['r_hopfion'], sim_params['sigma'], sim_params['center2'], sim_params['velocity2'], sim_params['phase2'])

    initial_field_x = hopfion1_x + hopfion2_x
    initial_field_y = hopfion1_y + hopfion2_y
    return initial_field_x, initial_field_y, dx, dy

# --- Visualization Functions ---
def animate_3d_turntable(fields, sim_params, filename="hopfion_turntable.gif"):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    isolevel_fraction = 0.4
    cmap = plt.get_cmap('coolwarm')
    norm = colors.Normalize(vmin=-1, vmax=1)

    field_x, field_y = fields
    total_intensity = np.abs(field_x)**2 + np.abs(field_y)**2
    s3_param = 2 * np.imag(np.conj(field_x) * field_y)
    s3_normalized = s3_param / (total_intensity + 1e-11)
    isolevel = total_intensity.max() * isolevel_fraction

    try:
        padded_intensity = np.pad(total_intensity, pad_width=1, mode='constant', constant_values=0)
        verts, faces, _, _ = marching_cubes(padded_intensity, level=isolevel)
        verts -= 1
        verts_scaled = -sim_params['sim_size'] + verts * (2 * sim_params['sim_size'] / (sim_params['grid_size'] - 1))
    except (ValueError, RuntimeError):
        click.echo("Turntable: Marching cubes failed. Cannot create animation.", err=True)
        plt.close(fig)
        return

    padded_s3 = np.pad(s3_normalized, pad_width=1, mode='constant', constant_values=0)
    s3_values_at_verts = map_coordinates(padded_s3, verts.T, order=1)
    face_s3_values = s3_values_at_verts[faces].mean(axis=1)
    face_colors = cmap(norm(face_s3_values))

    mesh = Poly3DCollection(verts_scaled[:, [1, 0, 2]][faces], facecolors=face_colors, edgecolor='k', linewidth=0.1, alpha=0.9)
    ax.add_collection3d(mesh)

    ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
    ax.set_xlim(-sim_params['sim_size'], sim_params['sim_size']); ax.set_ylim(-sim_params['sim_size'], sim_params['sim_size']); ax.set_zlim(-sim_params['sim_size'], sim_params['sim_size'])
    
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    fig.colorbar(sm, ax=ax, shrink=0.6, aspect=20).set_label('Normalized S3 Parameter')

    def update(frame_angle):
        ax.view_init(elev=30, azim=frame_angle)
        ax.set_title(f"3D Turntable View (Angle: {frame_angle:.1f}°)")
        click.echo(f"Rendering turntable frame at angle {frame_angle:.1f}°")
        return [mesh]

    angles = np.linspace(0, 360, 90)
    anim = animation.FuncAnimation(fig, update, frames=angles, blit=False)
    click.echo(f"Saving turntable animation to {filename}...")
    anim.save(filename, writer='pillow', fps=15, dpi=100)
    click.echo("Turntable animation saved.")
    plt.close(fig)

# --- CLI ---
@click.group()
def cli():
    """A CLI for simulating and visualizing Hopfion interactions."""
    pass

@cli.command()
@click.option('--grid-size', default=64, type=int, help='Grid size for the simulation.')
@click.option('--sim-size', default=10.0, type=float, help='Simulation box size.')
@click.option('--power', default=1.37e16, type=float, help='Optical power.')
@click.option('--num-steps', default=150, type=int, help='Number of simulation steps.')
@click.option('--store-interval', default=10, type=int, help='Interval to store simulation frames.')
@click.option('--velocity', default=5.0, type=float, help='Transverse velocity of hopfions.')
@click.option('--separation', default=5.0, type=float, help='Initial separation of hopfions.')
@click.option('--phase1', default=0.0, type=float, help='Initial phase of the first hopfion.')
@click.option('--phase2', default=0.0, type=float, help='Initial phase of the second hopfion.')
@click.option('--output-dir', default='results', help='Directory to save results.')
def run(grid_size, sim_size, power, num_steps, store_interval, velocity, separation, phase1, phase2, output_dir):
    """Runs the Hopfion interaction simulation and saves the results."""
    sim_params = {
        'grid_size': grid_size, 'sim_size': sim_size, 'power': power,
        'num_steps': num_steps, 'store_interval': store_interval,
        'r_hopfion': 1.0, 'sigma': 1.5, 'wavelength': 1.55,
        'n0_algaas': 3.3, 'n2_algaas': 1e-17, 'dz': 0.1,
        'separation': separation, 'velocity_x': velocity,
        'center1': (-separation / 2, 0, 0), 'velocity1': (velocity, 0), 'phase1': phase1,
        'center2': (separation / 2, 0, 0), 'velocity2': (-velocity, 0), 'phase2': phase2
    }
    
    click.echo("Creating initial field for two hopfions...")
    initial_field_x, initial_field_y, dx, dy = create_two_hopfions_initial_field(sim_params)

    k0 = 2 * np.pi / sim_params['wavelength']
    k = k0 * sim_params['n0_algaas']
    stored_fields = run_vnlse_simulation(
        initial_field_x, initial_field_y, dx, dy, sim_params['dz'], 
        sim_params['num_steps'], k, k0, sim_params['n2_algaas'], 
        store_interval=sim_params['store_interval']
    )

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"hopfion_interaction_{timestamp}.npz"
    filepath = os.path.join(output_dir, filename)
    
    click.echo(f"Saving simulation results to {filepath}...")
    np.savez_compressed(filepath, stored_fields=np.array(stored_fields, dtype=object), sim_params=sim_params)
    click.echo("Results saved.")

@cli.group()
def visualize():
    """Visualization commands."""
    pass

@visualize.command(name='turntable')
@click.argument('result_file', type=click.Path(exists=True))
@click.option('--frame', default=-1, type=int, help='Frame to visualize (-1 for last frame).')
def visualize_turntable(result_file, frame):
    """Creates a 3D turntable animation from a result file."""
    data = np.load(result_file, allow_pickle=True)
    stored_fields = data['stored_fields']
    sim_params = data['sim_params'].item()

    if not stored_fields.any() or frame >= len(stored_fields):
        click.echo(f"Invalid frame number. File contains {len(stored_fields)} frames.", err=True)
        return

    fields_to_visualize = stored_fields[frame]
    
    output_filename = f"turntable_frame{frame}_{os.path.basename(result_file).replace('.npz', '.gif')}"

    click.echo(f"\nCreating turntable animation for frame {frame} of {os.path.basename(result_file)}...")
    animate_3d_turntable(fields_to_visualize, sim_params, filename=output_filename)

if __name__ == '__main__':
    cli()