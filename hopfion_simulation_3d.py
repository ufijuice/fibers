import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# --- Core Simulation Function (Scalar NLSE) ---
def run_nlse_simulation(initial_field, dx, dy, dz, num_steps, k, k0, n2, output_filename="hopfion_propagation.gif"):
    """
    Solves the 3D NLSE using the split-step Fourier method and visualizes the result.
    """
    nx, ny, _ = initial_field.shape
    kx = 2 * np.pi * np.fft.fftfreq(nx, d=dx)
    ky = 2 * np.pi * np.fft.fftfreq(ny, d=dy)
    KX, KY = np.meshgrid(kx, ky)
    linear_operator = np.exp(-1j * (KX**2 + KY**2) / (2 * k) * dz / 2)

    field = initial_field.copy()
    field_history = [np.abs(field[:, :, field.shape[2] // 2])**2]

    for i in range(num_steps):
        # Linear step
        field_k = np.fft.fft2(field, axes=(0, 1))
        field_k *= linear_operator
        field = np.fft.ifft2(field_k, axes=(0, 1))
        # Nonlinear step
        field *= np.exp(1j * k0 * n2 * np.abs(field)**2 * dz)
        # Linear step
        field_k = np.fft.fft2(field, axes=(0, 1))
        field_k *= linear_operator
        field = np.fft.ifft2(field_k, axes=(0, 1))
        
        if (i + 1) % 5 == 0: # Store more frequently for animation
            field_history.append(np.abs(field[:, :, field.shape[2] // 2])**2)
            print(f"Step {i+1}/{num_steps} completed.")

    # --- Visualize Result ---
    print("Visualizing result...")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    x_vis = np.linspace(-5, 5, nx) # Adjusted spatial extent for visualization
    y_vis = np.linspace(-5, 5, ny)
    X_vis, Y_vis = np.meshgrid(x_vis, y_vis)

    def update_plot(frame, field_history, ax, dz):
        ax.clear()
        Z_vis = field_history[frame]
        ax.plot_surface(X_vis, Y_vis, Z_vis, cmap='viridis')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Intensity')
        ax.set_zlim(0, np.max(field_history[0])*2.0) # Keep z-axis scale constant, adjust dynamically
        ax.set_title(f'Intensity Profile at z = {frame * 5 * dz:.1f}')

    ani = animation.FuncAnimation(fig, update_plot, frames=len(field_history), fargs=(field_history, ax, dz), interval=100)
    
    try:
        ani.save(output_filename, writer='imagemagick')
        print(f"Animation saved to {output_filename}")
    except Exception as e:
        print(f"Could not save animation: {e}")
        print("Displaying animation instead.")
        plt.show()

# --- Initial Field Creation for Linked Vortices (Hopfion-like) ---
def create_initial_linked_vortex_field(grid_size, wavelength, power, n0_algaas, m1=1, m2=1, sigma=2.0):
    """
    Creates an initial scalar field with two linked vortices (Hopfion-like topology).
    """
    x = np.linspace(-5, 5, grid_size)
    y = np.linspace(-5, 5, grid_size)
    z = np.linspace(-5, 5, grid_size)
    X, Y, Z = np.meshgrid(x, y, z)
    dx = x[1] - x[0]
    dy = y[1] - y[0]

    # Amplitude profile (e.g., a Gaussian blob)
    amplitude = np.sqrt(power) * np.exp(-(X**2 + Y**2 + Z**2) / (2 * sigma**2))

    # Phase winding for two linked vortices
    # Vortex 1: along Z-axis, centered at (0, 0)
    phi1 = m1 * np.arctan2(Y, X + 1e-9) 
    
    # Vortex 2: along Y-axis, centered at (0, 0)
    phi2 = m2 * np.arctan2(Z, X + 1e-9)

    initial_field = amplitude * np.exp(1j * (phi1 + phi2))

    return initial_field, dx, dy

# --- Main Execution Block ---
if __name__ == '__main__':
    print("\n--- Simulating 3D Linked Vortex (Hopfion-like) Structure ---")
    # --- Simulation Parameters ---
    GRID_SIZE = 128 # Use a reasonable grid size for now
    WAVELENGTH = 1.55
    POWER = 1e3 # Start with high power, adjust as needed
    N0_ALGAAS = 3.3
    N2_ALGAAS = 1e-17
    DZ = 0.1
    NUM_STEPS = 200

    # --- Linked Vortex Parameters ---
    M1_CHARGE = 1 # Topological charge for first vortex
    M2_CHARGE = 1 # Topological charge for second vortex
    SIGMA = 2.0 # Size of the initial amplitude blob

    # --- Create Initial Field ---
    initial_field, dx, dy = create_initial_linked_vortex_field(
        GRID_SIZE, WAVELENGTH, POWER, N0_ALGAAS, m1=M1_CHARGE, m2=M2_CHARGE, sigma=SIGMA
    )

    # --- Run Simulation ---
    k0 = 2 * np.pi / WAVELENGTH
    k = k0 * N0_ALGAAS
    run_nlse_simulation(initial_field, dx, dy, DZ, NUM_STEPS, k, k0, N2_ALGAAS, output_filename="linked_vortex_propagation.gif")
