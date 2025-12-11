import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from skimage.measure import marching_cubes # For 3D isosurface visualization
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.colors as colors
from scipy.ndimage import map_coordinates

# --- Core Simulation Function ---
def run_vnlse_simulation(initial_field_x, initial_field_y, dx, dy, dz, num_steps, k, k0, n2):
    """
    Solves the 3D Vector NLSE (simplified).
    Returns the final Ex and Ey fields.
    """
    nx, ny, nz = initial_field_x.shape
    kx = 2 * np.pi * np.fft.fftfreq(nx, d=dx)
    ky = 2 * np.pi * np.fft.fftfreq(ny, d=dy)
    KX, KY = np.meshgrid(kx, ky)
    linear_operator = np.exp(-1j * (KX**2 + KY**2) / (2 * k) * dz / 2)

    field_x = initial_field_x.copy()
    field_y = initial_field_y.copy()

    gamma = k0 * n2 # Nonlinear coefficient

    print("Running VNLSE simulation...")
    for i in range(num_steps):
        # Linear step (applied independently to each component)
        field_x_k = np.fft.fft2(field_x, axes=(0, 1))
        field_x_k *= linear_operator
        field_x = np.fft.ifft2(field_x_k, axes=(0, 1))

        field_y_k = np.fft.fft2(field_y, axes=(0, 1))
        field_y_k *= linear_operator
        field_y = np.fft.ifft2(field_y_k, axes=(0, 1))

        # Nonlinear step (coupled equations for self- and cross-phase modulation)
        abs_field_x_sq = np.abs(field_x)**2
        abs_field_y_sq = np.abs(field_y)**2

        # Full VNLSE nonlinear terms (including four-wave mixing, robust form)
        field_x *= np.exp(1j * gamma * (abs_field_x_sq + (2/3) * abs_field_y_sq + (1/3) * np.abs(field_y)**2 * np.cos(2 * np.angle(field_y) - 2 * np.angle(field_x))) * dz)
        field_y *= np.exp(1j * gamma * (abs_field_y_sq + (2/3) * abs_field_x_sq + (1/3) * np.abs(field_x)**2 * np.cos(2 * np.angle(field_x) - 2 * np.angle(field_y))) * dz)

        # Second half linear step (applied independently)
        field_x_k = np.fft.fft2(field_x, axes=(0, 1))
        field_x_k *= linear_operator
        field_x = np.fft.ifft2(field_x_k, axes=(0, 1))

        field_y_k = np.fft.fft2(field_y, axes=(0, 1))
        field_y_k *= linear_operator
        field_y = np.fft.ifft2(field_y_k, axes=(0, 1))
        
        if (i + 1) % 20 == 0: # Print progress less frequently
            print(f"Step {i+1}/{num_steps} completed.")

    return field_x, field_y

# --- Initial Field Creation for Hopfion ---
def create_initial_hopfion_field_vector(grid_size, wavelength, power, n0_algaas, R_hopfion=1.0, sigma=1.0):
    """
    Creates initial Ex and Ey fields with Hopfion topology based on a rational map.
    """
    x = np.linspace(-5, 5, grid_size)
    y = np.linspace(-5, 5, grid_size)
    z = np.linspace(-5, 5, grid_size)
    X, Y, Z = np.meshgrid(x, y, z)
    dx = x[1] - x[0]
    dy = y[1] - y[0]

    # Complex coordinates for Hopfion construction
    u = X + 1j * Y
    v = Z + 1j * R_hopfion
    
    psi1_raw = (u + 1j * v)
    psi2_raw = (v + 1j * np.conj(u))

    # Normalize the total intensity to the desired power
    total_intensity_norm = np.sqrt(np.abs(psi1_raw)**2 + np.abs(psi2_raw)**2)
    total_intensity_norm[total_intensity_norm < 1e-9] = 1e-9 # Avoid division by zero

    # Initial Ex and Ey fields with Hopfion winding
    initial_field_x = np.sqrt(power) * (psi1_raw / total_intensity_norm) * np.exp(-(X**2 + Y**2) / (2 * sigma**2))
    initial_field_y = np.sqrt(power) * (psi2_raw / total_intensity_norm) * np.exp(-(X**2 + Y**2) / (2 * sigma**2))

    return initial_field_x, initial_field_y, dx, dy

# --- 2D Slices of Initial Hopfion Visualization ---
def visualize_initial_hopfion_2d_slices(field_x, field_y, grid_size, title="Initial Hopfion Structure (2D Slices)"):
    """
    Visualizes 2D contour plots of total intensity and phase at different Z slices.
    """
    x = np.linspace(-5, 5, grid_size)
    y = np.linspace(-5, 5, grid_size)
    z = np.linspace(-5, 5, grid_size)
    
    total_intensity = np.abs(field_x)**2 + np.abs(field_y)**2
    phase_ex = np.angle(field_x)

    # Choose a few Z slices to visualize
    z_indices = [0, grid_size // 4, grid_size // 2, 3 * grid_size // 4, grid_size - 1]
    z_values = [z[idx] for idx in z_indices]

    fig, axes = plt.subplots(2, len(z_indices), figsize=(4 * len(z_indices), 8))
    if len(z_indices) == 1: # Handle case of single subplot
        axes = np.array([[axes[0]], [axes[1]]]) # Make it 2x1 for consistency

    for i, z_idx in enumerate(z_indices):
        # Intensity slices
        ax_int = axes[0, i]
        intensity_slice = total_intensity[:, :, z_idx]
        ax_int.contourf(x, y, intensity_slice, levels=50, cmap='viridis')
        ax_int.set_title(f'Z = {z_values[i]:.1f}')
        ax_int.set_xlabel('X')
        ax_int.set_ylabel('Y')
        ax_int.set_aspect('equal', adjustable='box')
        if i == 0:
            ax_int.set_ylabel('Total Intensity')

        # Phase slices
        ax_phase = axes[1, i]
        phase_slice = phase_ex[:, :, z_idx]
        ax_phase.contourf(x, y, phase_slice, levels=50, cmap='hsv') # hsv for phase
        ax_phase.set_xlabel('X')
        ax_phase.set_ylabel('Y')
        ax_phase.set_aspect('equal', adjustable='box')
        if i == 0:
            ax_phase.set_ylabel('Phase (Ex)')

    fig.suptitle(title)
    plt.tight_layout()
    plt.show()


def visualize_3d_intensity(field_x, field_y, grid_size, sim_params, title="3D Intensity Isosurface with Polarization", isolevel_fraction=0.5):
    """
    Visualizes a 3D isosurface of the total field intensity, colored by the
    S3 Stokes parameter to show polarization twist (the Hopfion structure).
    Saves the output to a file with simulation parameters in the name.
    """
    # --- 1. Calculate Stokes Parameters ---
    total_intensity = np.abs(field_x)**2 + np.abs(field_y)**2 # This is S0
    # S3 = 2 * Im(Ex* Ey)
    s3_param = 2 * np.imag(np.conj(field_x) * field_y)
    
    # Normalize s3 by the total intensity to get a value between -1 and 1
    s3_normalized = s3_param / (total_intensity + 1e-11)

    # --- 2. Get Isosurface using Marching Cubes ---
    isolevel = total_intensity.max() * isolevel_fraction
    
    # Pad the volume with zeros so that the isosurface is closed.
    padded_intensity = np.pad(total_intensity, pad_width=1, mode='constant', constant_values=0)

    try:
        verts, faces, _, _ = marching_cubes(padded_intensity, level=isolevel, spacing=(1.0, 1.0, 1.0))
        # Adjust vertices to account for padding
        verts -= 1
    except (ValueError, RuntimeError) as e:
        print(f"Marching cubes failed: {e}. Falling back to 2D slices.")
        visualize_initial_hopfion_2d_slices(field_x, field_y, grid_size, title="Fallback 2D Slices")
        return

    # --- 3. Color the Isosurface with the S3 Parameter ---
    # Pad the s3 field to match the padded intensity field
    padded_s3 = np.pad(s3_normalized, pad_width=1, mode='constant', constant_values=0)
    
    # The vertices from marching_cubes are in the coordinates of the padded array.
    # We need to find the value of s3 at each vertex.
    # `map_coordinates` is used for interpolation at non-grid points.
    # The coordinates need to be transposed for map_coordinates.
    s3_values_at_verts = map_coordinates(padded_s3, verts.T, order=1)

    # Calculate the color for each face by averaging the s3 values of its vertices
    face_s3_values = s3_values_at_verts[faces].mean(axis=1)

    # --- 4. Create 3D Plot ---
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')

    # Create a mesh collection. This is more flexible than plot_trisurf.
    mesh = Poly3DCollection(verts[faces])

    # Set face colors based on the s3 values using a colormap
    # We use a diverging colormap since s3 goes from -1 to 1
    cmap = plt.get_cmap('coolwarm')
    # Auto-scale the color normalization to the actual data range on the surface
    vmin = face_s3_values.min()
    vmax = face_s3_values.max()
    norm = colors.Normalize(vmin=vmin, vmax=vmax)
    face_colors = cmap(norm(face_s3_values))
    mesh.set_facecolor(face_colors)
    mesh.set_edgecolor('k') # Add black edges for definition
    mesh.set_linewidth(0.1)
    mesh.set_alpha(0.9)

    ax.add_collection3d(mesh)

    ax.set_title(title)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    # Add a color bar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array(face_s3_values)
    cbar = fig.colorbar(sm, ax=ax, shrink=0.6, aspect=20)
    cbar.set_label('Normalized S3 Parameter (Polarization)')

    # Set aspect ratio to be equal
    max_range = np.array([verts[:, 0].max()-verts[:, 0].min(), 
                          verts[:, 1].max()-verts[:, 1].min(), 
                          verts[:, 2].max()-verts[:, 2].min()]).max() / 2.0

    mid_x = (verts[:, 0].max()+verts[:, 0].min()) * 0.5
    mid_y = (verts[:, 1].max()+verts[:, 1].min()) * 0.5
    mid_z = (verts[:, 2].max()+verts[:, 2].min()) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    # --- 5. Save File ---
    filename = (f"hopfion_P{sim_params['power']:.2e}_GS{sim_params['grid_size']}"
                f"_N{sim_params['num_steps']}_R{sim_params['r_hopfion']}"
                f"_S{sim_params['sigma']}.png")
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Visualization saved to {filename}")
    plt.close(fig)


# --- Main Execution Block ---
if __name__ == '__main__':
    # --- Simulation Parameters ---
    GRID_SIZE = 128 # Increased for full simulation
    WAVELENGTH = 1.55
    POWER = 1.37e16 # 1.37e16 knot is visible
    N0_ALGAAS = 3.3
    N2_ALGAAS = 1e-17
    DZ = 0.1
    NUM_STEPS = 200 # Increased for full simulation

    # --- Hopfion Parameters ---
    R_HOPFION = 1.0 # Radius parameter for Hopfion
    SIGMA = 1.0 # Size of the initial amplitude blob

    # --- Create a dictionary of parameters for saving ---
    sim_params = {
        'grid_size': GRID_SIZE,
        'power': POWER,
        'num_steps': NUM_STEPS,
        'r_hopfion': R_HOPFION,
        'sigma': SIGMA,
    }

    # --- Create Initial Field ---
    print("Creating initial field...")
    initial_field_x, initial_field_y, dx, dy = create_initial_hopfion_field_vector(
        GRID_SIZE, WAVELENGTH, POWER, N0_ALGAAS, R_hopfion=R_HOPFION, sigma=SIGMA
    )

    # --- Run Simulation ---
    k0 = 2 * np.pi / WAVELENGTH
    k = k0 * N0_ALGAAS
    final_field_x, final_field_y = run_vnlse_simulation(
        initial_field_x, initial_field_y, dx, dy, DZ, NUM_STEPS, k, k0, N2_ALGAAS)

    # --- Visualize Final 3D Intensity ---
    print("Visualizing final 3D intensity structure...")
    visualize_3d_intensity(
        final_field_x, 
        final_field_y, 
        GRID_SIZE, 
        sim_params,
        title="3D Hopfion Intensity and Polarization"
    )
