import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

def split_step_fourier_3d(initial_field, dx, dy, dz, num_steps, k, k0, n2):
    """
    Solves the 3D Nonlinear Schrödinger Equation using the split-step Fourier method.

    Args:
        initial_field (np.ndarray): The initial 3D electric field envelope.
        dx (float): The grid spacing in the x direction.
        dy (float): The grid spacing in the y direction.
        dz (float): The step size in the z direction.
        num_steps (int): The number of propagation steps.
        k (float): The wave number.
        k0 (float): The wave number in vacuum.
        n2 (float): The nonlinear refractive index.

    Returns:
        np.ndarray: The 3D field at the final propagation step.
        list: A list of the 3D field at each propagation step.
    """
    nx, ny, _ = initial_field.shape
    kx = 2 * np.pi * np.fft.fftfreq(nx, d=dx)
    ky = 2 * np.pi * np.fft.fftfreq(ny, d=dy)
    KX, KY = np.meshgrid(kx, ky)

    # Linear operator (diffraction)
    linear_operator = np.exp(-1j * (KX**2 + KY**2) / (2 * k) * dz / 2)

    field = initial_field.copy()
    field_history = [np.abs(field[:, :, field.shape[2] // 2])**2]

    for i in range(num_steps):
        # First half linear step
        field_k = np.fft.fft2(field, axes=(0, 1))
        field_k *= linear_operator
        field = np.fft.ifft2(field_k, axes=(0, 1))

        # Nonlinear step
        field *= np.exp(1j * k0 * n2 * np.abs(field)**2 * dz)

        # Second half linear step
        field_k = np.fft.fft2(field, axes=(0, 1))
        field_k *= linear_operator
        field = np.fft.ifft2(field_k, axes=(0, 1))
        
        # Store the field at the middle slice for visualization
        if (i + 1) % 10 == 0: # Store every 10 steps
            field_history.append(np.abs(field[:, :, field.shape[2] // 2])**2)
            print(f"Step {i+1}/{num_steps} completed.")

    return field, field_history

def create_initial_field(grid_size=128, beam_waist=1.0, wavelength=1.55, power=1e6, n0_algaas=3.3):
    """
    Creates the initial field for the simulation (interference of two beams).
    """
    x = np.linspace(-5, 5, grid_size)
    y = np.linspace(-5, 5, grid_size)
    z = np.linspace(-5, 5, grid_size)
    X, Y, Z = np.meshgrid(x, y, z)
    dx = x[1] - x[0]
    dy = y[1] - y[0]

    k_vac = 2 * np.pi / wavelength
    
    # For simplicity, we create two slightly angled beams
    angle = 0.1
    E1 = np.sqrt(power) * np.exp(-(X**2 + Y**2) / beam_waist**2) * np.exp(1j * k_vac * n0_algaas * (Z * np.cos(angle) + X * np.sin(angle)))
    E2 = np.sqrt(power) * np.exp(-(X**2 + Y**2) / beam_waist**2) * np.exp(1j * k_vac * n0_algaas * (Z * np.cos(angle) - X * np.sin(angle)))

    return E1 + E2, dx, dy

if __name__ == '__main__':
    # --- Simulation Parameters ---
    GRID_SIZE = 128
    BEAM_WAIST = 1.0
    WAVELENGTH = 1.55  # Micrometers
    POWER = 2e16 # the effect starts to happen on 2e16
    N0_ALGAAS = 3.3
    N2_ALGAAS = 1e-17  # m^2/W
    
    DZ = 0.1 # Propagation step size
    NUM_STEPS = 500 # Number of steps

    # --- Create Initial Field ---
    print("Creating initial field...")
    initial_field, dx, dy = create_initial_field(
        grid_size=GRID_SIZE,
        beam_waist=BEAM_WAIST,
        wavelength=WAVELENGTH,
        power=POWER,
        n0_algaas=N0_ALGAAS
    )

    # --- Run Simulation ---
    print("Running NLSE simulation...")
    k0 = 2 * np.pi / WAVELENGTH
    k = k0 * N0_ALGAAS
    final_field, field_history = split_step_fourier_3d(
        initial_field, dx, dy, DZ, NUM_STEPS, k, k0, N2_ALGAAS
    )

    # --- Visualize Results ---
    print("Visualizing results...")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    x_vis = np.linspace(-5, 5, GRID_SIZE)
    y_vis = np.linspace(-5, 5, GRID_SIZE)
    X_vis, Y_vis = np.meshgrid(x_vis, y_vis)

    def update_plot(frame, field_history, ax):
        ax.clear()
        Z_vis = field_history[frame]
        ax.plot_surface(X_vis, Y_vis, Z_vis, cmap='viridis')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Intensity')
        ax.set_title(f'Intensity Profile at z = {frame * 10 * DZ:.1f}')

    ani = animation.FuncAnimation(fig, update_plot, frames=len(field_history), fargs=(field_history, ax), interval=100)
    
    try:
        ani.save('hopf_soliton_propagation.gif', writer='imagemagick')
        print("Animation saved to hopf_soliton_propagation.gif")
    except Exception as e:
        print(f"Could not save animation: {e}")
        print("Displaying animation instead.")
        plt.show()

