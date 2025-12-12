import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from skimage.measure import marching_cubes # For 3D isosurface visualization
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.colors as colors
from scipy.ndimage import map_coordinates

# --- Core Simulation Function ---
def run_vnlse_simulation(initial_field_x, initial_field_y, dx, dy, dz, num_steps, k, k0, n2, store_interval=10):
    """
    Solves the 3D Vector NLSE (simplified).
    Returns a list of stored fields at specified intervals.
    """
    nx, ny, nz = initial_field_x.shape
    kx = 2 * np.pi * np.fft.fftfreq(nx, d=dx)
    ky = 2 * np.pi * np.fft.fftfreq(ny, d=dy)
    KX, KY = np.meshgrid(kx, ky)
    linear_operator = np.exp(-1j * (KX**2 + KY**2) / (2 * k) * dz / 2)

    field_x = initial_field_x.copy()
    field_y = initial_field_y.copy()

    gamma = k0 * n2 # Nonlinear coefficient

    stored_fields = []

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
        
        if (i + 1) % store_interval == 0:
            stored_fields.append((field_x.copy(), field_y.copy()))
            print(f"Step {i+1}/{num_steps} completed. Storing fields.")

    return stored_fields

# --- Initial Field Creation for a Single Hopfion ---
def create_single_hopfion(grid, power, R_hopfion=1.0, sigma=1.0, center=(0,0,0), velocity=(0,0)):
    """
    Creates the fields for a single hopfion at a specified center and with a given velocity.
    """
    X, Y, Z = grid
    x0, y0, z0 = center
    vx, vy = velocity

    # Shift coordinates to the center of the hopfion
    X_shifted, Y_shifted, Z_shifted = X - x0, Y - y0, Z - z0

    # Complex coordinates for Hopfion construction
    u = X_shifted + 1j * Y_shifted
    v = Z_shifted + 1j * R_hopfion
    
    psi1_raw = (u + 1j * v)
    psi2_raw = (v + 1j * np.conj(u))

    # Normalize the total intensity
    total_intensity_norm = np.sqrt(np.abs(psi1_raw)**2 + np.abs(psi2_raw)**2)
    total_intensity_norm[total_intensity_norm < 1e-9] = 1e-9 # Avoid division by zero

    # Gaussian amplitude profile
    amplitude_profile = np.exp(-(X_shifted**2 + Y_shifted**2 + Z_shifted**2) / (2 * sigma**2))

    # Initial Ex and Ey fields with Hopfion winding
    field_x = np.sqrt(power) * (psi1_raw / total_intensity_norm) * amplitude_profile
    field_y = np.sqrt(power) * (psi2_raw / total_intensity_norm) * amplitude_profile

    # Add velocity by applying a phase ramp
    phase_ramp = np.exp(1j * (vx * X_shifted + vy * Y_shifted))
    field_x *= phase_ramp
    field_y *= phase_ramp

    return field_x, field_y

# --- Initial Field Creation for Two Hopfions ---
def create_two_hopfions_initial_field(grid_size, sim_size, power, R_hopfion=1.0, sigma=1.0, center1=(0,0,0), velocity1=(0,0), center2=(0,0,0), velocity2=(0,0)):
    """
    Creates the initial field for two interacting hopfions.
    """
    # Create a grid of points
    x = np.linspace(-sim_size, sim_size, grid_size)
    y = np.linspace(-sim_size, sim_size, grid_size)
    z = np.linspace(-sim_size, sim_size, grid_size)
    X, Y, Z = np.meshgrid(x, y, z)
    grid = (X, Y, Z)
    dx = x[1] - x[0]
    dy = y[1] - y[0]

    # Create the first hopfion
    hopfion1_x, hopfion1_y = create_single_hopfion(grid, power, R_hopfion, sigma, center1, velocity1)

    # Create the second hopfion
    hopfion2_x, hopfion2_y = create_single_hopfion(grid, power, R_hopfion, sigma, center2, velocity2)

    # Superimpose the fields
    initial_field_x = hopfion1_x + hopfion2_x
    initial_field_y = hopfion1_y + hopfion2_y

    return initial_field_x, initial_field_y, dx, dy


# --- Animation Function ---
def animate_2d_slice_interaction(stored_fields, sim_params, filename="hopfion_interaction.gif"):
    """
    Creates an animated GIF of the 2D central slice of the interaction.
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    
    grid_size = sim_params['grid_size']
    sim_size = sim_params['sim_size']
    
    # Get the first frame to set up the plot
    field_x, field_y = stored_fields[0]
    total_intensity = np.abs(field_x)**2 + np.abs(field_y)**2
    central_slice_idx = grid_size // 2
    intensity_slice = total_intensity[:, :, central_slice_idx]
    
    im = ax.imshow(intensity_slice.T, origin='lower', extent=[-sim_size, sim_size, -sim_size, sim_size], cmap='viridis', animated=True)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label('Total Intensity')

    def update(frame):
        field_x, field_y = stored_fields[frame]
        total_intensity = np.abs(field_x)**2 + np.abs(field_y)**2
        intensity_slice = total_intensity[:, :, central_slice_idx]
        
        im.set_array(intensity_slice.T)
        im.set_clim(vmin=intensity_slice.min(), vmax=intensity_slice.max()) # Rescale colorbar for each frame
        ax.set_title(f"Interaction at Z=0, Step {frame * sim_params['store_interval']}")
        return im,

    anim = animation.FuncAnimation(fig, update, frames=len(stored_fields), blit=True)
    
    print(f"Saving animation to {filename}...")
    anim.save(filename, writer='pillow', fps=10)
    print("Animation saved.")
    plt.close(fig)


# --- Main Execution Block ---
if __name__ == '__main__':
    # --- Simulation Parameters ---
    GRID_SIZE = 128 # Keep it reasonable for performance
    SIM_SIZE = 10.0 # Increased simulation box size
    WAVELENGTH = 1.55
    POWER = 0.5e16 
    N0_ALGAAS = 3.3
    N2_ALGAAS = 1e-17
    DZ = 0.1
    NUM_STEPS = 400 # Increased steps to see the interaction
    STORE_INTERVAL = 5 # Store fields every 5 steps

    # --- Hopfion Parameters ---
    R_HOPFION = 1.0 
    SIGMA = 1.5 # Slightly larger sigma

    # --- Interaction Parameters ---
    separation = 5.0 # Initial separation on the x-axis
    center1 = (-separation / 2, 0, 0)
    center2 = (separation / 2, 0, 0)
    
    velocity_x = 5.0 # Transverse velocity
    velocity1 = (velocity_x, 0)
    velocity2 = (-velocity_x, 0)

    # --- Create a dictionary of parameters for saving ---
    sim_params = {
        'grid_size': GRID_SIZE,
        'sim_size': SIM_SIZE,
        'power': POWER,
        'num_steps': NUM_STEPS,
        'store_interval': STORE_INTERVAL,
        'r_hopfion': R_HOPFION,
        'sigma': SIGMA,
        'separation': separation,
        'velocity_x': velocity_x
    }

    # --- Create Initial Field ---
    print("Creating initial field for two hopfions...")
    initial_field_x, initial_field_y, dx, dy = create_two_hopfions_initial_field(
        grid_size=GRID_SIZE,
        sim_size=SIM_SIZE,
        power=POWER,
        R_hopfion=R_HOPFION,
        sigma=SIGMA,
        center1=center1,
        velocity1=velocity1,
        center2=center2,
        velocity2=velocity2
    )

    # --- Run Simulation ---
    k0 = 2 * np.pi / WAVELENGTH
    k = k0 * N0_ALGAAS
    stored_fields = run_vnlse_simulation(
        initial_field_x, initial_field_y, dx, dy, DZ, NUM_STEPS, k, k0, N2_ALGAAS, store_interval=STORE_INTERVAL)

    # --- Animate Final Result ---
    print("Creating animation of the interaction...")
    animate_2d_slice_interaction(
        stored_fields, 
        sim_params,
        filename="hopfion_interaction.gif"
    )
