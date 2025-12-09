import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# --- Core Simulation Function ---
def run_nlse_simulation(initial_field, dx, dy, dz, num_steps, k, k0, n2, output_filename="soliton_gate_collision.gif"):
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
    
    x_vis = np.linspace(-10, 10, nx)
    y_vis = np.linspace(-10, 10, ny)
    X_vis, Y_vis = np.meshgrid(x_vis, y_vis)

    def update_plot(frame, field_history, ax, DZ):
        ax.clear()
        Z_vis = field_history[frame]
        ax.plot_surface(X_vis, Y_vis, Z_vis, cmap='viridis')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Intensity')
        ax.set_zlim(0, 2e16) # Keep z-axis scale constant
        ax.set_title(f'Intensity Profile at z = {frame * 5 * DZ:.1f}')

    ani = animation.FuncAnimation(fig, update_plot, frames=len(field_history), fargs=(field_history, ax, dz), interval=100)
    
    try:
        ani.save(output_filename, writer='imagemagick')
        print(f"Animation saved to {output_filename}")
    except Exception as e:
        print(f"Could not save animation: {e}")
        print("Displaying animation instead.")
        plt.show()

# --- Initial Field Creation ---
def create_initial_field_for_gate(grid_size, beam_waist, wavelength, power, n0_algaas, separation, angle, input_a=1, input_b=1):
    """
    Creates the initial field for the gate simulation based on inputs.
    input_a, input_b: 1 for soliton present, 0 for no soliton.
    """
    x = np.linspace(-10, 10, grid_size)
    y = np.linspace(-10, 10, grid_size)
    z = np.linspace(-10, 10, grid_size)
    X, Y, Z = np.meshgrid(x, y, z)
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    k_vac = 2 * np.pi / wavelength

    initial_field = np.zeros_like(X, dtype=complex)

    # Soliton A (Input A)
    if input_a == 1:
        X_a = X + separation / 2
        soliton_a = np.sqrt(power) * np.exp(-(X_a**2 + Y**2) / beam_waist**2) * np.exp(-1j * k_vac * n0_algaas * X_a * np.tan(angle))
        initial_field += soliton_a
    
    # Soliton B (Input B)
    if input_b == 1:
        X_b = X - separation / 2
        soliton_b = np.sqrt(power) * np.exp(-(X_b**2 + Y**2) / beam_waist**2) * np.exp(1j * k_vac * n0_algaas * X_b * np.tan(angle))
        initial_field += soliton_b

    return initial_field, dx, dy

# --- Gate Simulation Functions ---
def simulate_and_gate_1_and_1():
    print("\n--- Simulating AND Gate: Input 1 AND 1 ---")
    # --- Simulation Parameters ---
    GRID_SIZE = 128
    BEAM_WAIST = 1.0
    WAVELENGTH = 1.55
    POWER = 2.00e15
    N0_ALGAAS = 3.3
    N2_ALGAAS = 1e-17
    DZ = 0.2
    NUM_STEPS = 200

    # --- Gate Parameters ---
    SEPARATION = 5.0
    ANGLE = -0.1  # Angle you discovered for merging

    # --- Create Initial Field ---
    initial_field, dx, dy = create_initial_field_for_gate(
        GRID_SIZE, BEAM_WAIST, WAVELENGTH, POWER, N0_ALGAAS, SEPARATION, ANGLE, input_a=1, input_b=1
    )

    # --- Run Simulation ---
    k0 = 2 * np.pi / WAVELENGTH
    k = k0 * N0_ALGAAS
    run_nlse_simulation(initial_field, dx, dy, DZ, NUM_STEPS, k, k0, N2_ALGAAS, output_filename="soliton_and_gate_1_and_1.gif")

def simulate_and_gate_1_and_0():
    print("\n--- Simulating AND Gate: Input 1 AND 0 ---")
    # --- Simulation Parameters ---
    GRID_SIZE = 128
    BEAM_WAIST = 1.0
    WAVELENGTH = 1.55
    POWER = 2.00e15
    N0_ALGAAS = 3.3
    N2_ALGAAS = 1e-17
    DZ = 0.2
    NUM_STEPS = 200

    # --- Gate Parameters ---
    SEPARATION = 5.0
    ANGLE = -0.1  # Angle you discovered for merging

    # --- Create Initial Field ---
    initial_field, dx, dy = create_initial_field_for_gate(
        GRID_SIZE, BEAM_WAIST, WAVELENGTH, POWER, N0_ALGAAS, SEPARATION, ANGLE, input_a=1, input_b=0
    )

    # --- Run Simulation ---
    k0 = 2 * np.pi / WAVELENGTH
    k = k0 * N0_ALGAAS
    run_nlse_simulation(initial_field, dx, dy, DZ, NUM_STEPS, k, k0, N2_ALGAAS, output_filename="soliton_and_gate_1_and_0.gif")

def simulate_and_gate_0_and_0():
    print("\n--- Simulating AND Gate: Input 0 AND 0 ---")
    # --- Simulation Parameters ---
    GRID_SIZE = 128
    BEAM_WAIST = 1.0
    WAVELENGTH = 1.55
    POWER = 2.00e15
    N0_ALGAAS = 3.3
    N2_ALGAAS = 1e-17
    DZ = 0.2
    NUM_STEPS = 200

    # --- Gate Parameters ---
    SEPARATION = 5.0
    ANGLE = -0.1  # Angle you discovered for merging

    # --- Create Initial Field ---
    initial_field, dx, dy = create_initial_field_for_gate(
        GRID_SIZE, BEAM_WAIST, WAVELENGTH, POWER, N0_ALGAAS, SEPARATION, ANGLE, input_a=0, input_b=0
    )

    # --- Run Simulation ---
    k0 = 2 * np.pi / WAVELENGTH
    k = k0 * N0_ALGAAS
    run_nlse_simulation(initial_field, dx, dy, DZ, NUM_STEPS, k, k0, N2_ALGAAS, output_filename="soliton_and_gate_0_and_0.gif")


# --- Main Execution Block ---
if __name__ == '__main__':
    # Choose which gate case to simulate
    # Options: "1_and_1", "1_and_0", "0_and_0"
    GATE_TO_SIMULATE = "0_and_0" 

    if GATE_TO_SIMULATE == "1_and_1":
        simulate_and_gate_1_and_1()
    elif GATE_TO_SIMULATE == "1_and_0":
        simulate_and_gate_1_and_0()
    elif GATE_TO_SIMULATE == "0_and_0":
        simulate_and_gate_0_and_0()
    else:
        print("Invalid GATE_TO_SIMULATE specified. Please choose '1_and_1', '1_and_0', or '0_and_0'.")