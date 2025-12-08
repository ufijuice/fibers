import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

def split_step_fourier_3d(initial_field, dx, dy, dz, num_steps, k, k0, n2):
    """
    Solves the 3D Nonlinear Schrödinger Equation using the split-step Fourier method.
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
        
        if (i + 1) % 10 == 0:
            field_history.append(np.abs(field[:, :, field.shape[2] // 2])**2)
            print(f"Step {i+1}/{num_steps} completed.")

    return field_history

def create_initial_field(grid_size, beam_waist, wavelength, power, n0_algaas):
    """
    Creates the initial field for the simulation.
    """
    x = np.linspace(-5, 5, grid_size)
    y = np.linspace(-5, 5, grid_size)
    z = np.linspace(-5, 5, grid_size)
    X, Y, Z = np.meshgrid(x, y, z)
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    k_vac = 2 * np.pi / wavelength
    angle = 0.1
    E1 = np.sqrt(power) * np.exp(-(X**2 + Y**2) / beam_waist**2) * np.exp(1j * k_vac * n0_algaas * (Z * np.cos(angle) + X * np.sin(angle)))
    E2 = np.sqrt(power) * np.exp(-(X**2 + Y**2) / beam_waist**2) * np.exp(1j * k_vac * n0_algaas * (Z * np.cos(angle) - X * np.sin(angle)))
    return E1 + E2, dx, dy

if __name__ == '__main__':
    # --- Final Simulation Parameters ---
    GRID_SIZE = 128 # Back to high resolution
    BEAM_WAIST = 1.0
    WAVELENGTH = 1.55
    POWER = 2.00e15  # The optimal power we discovered!
    N0_ALGAAS = 3.3
    N2_ALGAAS = 1e-17
    DZ = 0.1
    NUM_STEPS = 500 # Back to long simulation

    # --- Create Initial Field ---
    print("Creating initial field for final simulation...")
    initial_field, dx, dy = create_initial_field(
        GRID_SIZE, BEAM_WAIST, WAVELENGTH, POWER, N0_ALGAAS
    )

    # --- Run Simulation ---
    print(f"Running final simulation with optimal POWER = {POWER:.2e}...")
    k0 = 2 * np.pi / WAVELENGTH
    k = k0 * N0_ALGAAS
    field_history = split_step_fourier_3d(
        initial_field, dx, dy, DZ, NUM_STEPS, k, k0, N2_ALGAAS
    )

    # --- Visualize Final Result ---
    print("Visualizing final result...")
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
        ani.save('final_soliton_propagation.gif', writer='imagemagick')
        print("Animation saved to final_soliton_propagation.gif")
    except Exception as e:
        print(f"Could not save animation: {e}")
        print("Displaying animation instead.")
        plt.show()
