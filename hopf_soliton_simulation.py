import numpy as np
import matplotlib.pyplot as plt

def create_hopf_soliton(grid_size=100, beam_waist=1.0, wavelength1=0.8, wavelength2=1.2, k_val=1.0, time=0.0):
    """
    Simulates the creation of a Hopf soliton using two interfering light beams.

    Args:
        grid_size (int): The resolution of the simulation grid.
        beam_waist (float): The waist of the Gaussian beams.
        wavelength1 (float): The wavelength of the first beam.
        wavelength2 (float): The wavelength of the second beam.
        k_val (float): The wave vector component.
        time (float): The time at which to evaluate the fields.

    Returns:
        tuple: A tuple containing the grid coordinates (X, Y, Z) and the Stokes parameters (S0, S1, S2, S3).
    """
    # Create a grid of points
    x = np.linspace(-2, 2, grid_size)
    y = np.linspace(-2, 2, grid_size)
    z = np.linspace(-2, 2, grid_size)
    X, Y, Z = np.meshgrid(x, y, z)

    # Wave numbers
    k1 = 2 * np.pi / wavelength1
    k2 = 2 * np.pi / wavelength2

    # Gouy phase
    z_R1 = np.pi * beam_waist**2 / wavelength1
    z_R2 = np.pi * beam_waist**2 / wavelength2
    gouy_phase1 = np.arctan(Z / z_R1)
    gouy_phase2 = np.arctan(Z / z_R2)

    # Beam radius
    w_z1 = beam_waist * np.sqrt(1 + (Z / z_R1)**2)
    w_z2 = beam_waist * np.sqrt(1 + (Z / z_R2)**2)

    # Radial distance
    r = np.sqrt(X**2 + Y**2)

    # Amplitudes
    A1 = (beam_waist / w_z1) * np.exp(-r**2 / w_z1**2)
    A2 = (beam_waist / w_z2) * np.exp(-r**2 / w_z2**2)

    # Electric fields (complex)
    E1 = A1 * np.exp(1j * (k1 * Z - k1 * time + gouy_phase1))
    E2 = A2 * np.exp(1j * (k2 * Z - k2 * time + gouy_phase2))

    # Total field
    E_total = E1 + E2

    # Stokes parameters
    S0 = np.abs(E1)**2 + np.abs(E2)**2
    S1 = 2 * np.real(np.conj(E1) * E2)
    S2 = -2 * np.imag(np.conj(E1) * E2)
    S3 = np.abs(E1)**2 - np.abs(E2)**2
    
    # Normalize Stokes vector
    norm = np.sqrt(S1**2 + S2**2 + S3**2)
    norm[norm == 0] = 1
    S1 /= norm
    S2 /= norm
    S3 /= norm


    return (X, Y, Z), (S0, S1, S2, S3)

def visualize_hopf_soliton(grid, stokes_parameters, slice_axis='z', slice_index=None):
    """
    Visualizes a slice of the Hopf soliton.

    Args:
        grid (tuple): The grid coordinates (X, Y, Z).
        stokes_parameters (tuple): The Stokes parameters (S0, S1, S2, S3).
        slice_axis (str): The axis to slice along ('x', 'y', or 'z').
        slice_index (int): The index of the slice. If None, the middle slice is used.
    """
    X, Y, Z = grid
    S0, S1, S2, S3 = stokes_parameters

    if slice_index is None:
        slice_index = S1.shape[0] // 2

    if slice_axis == 'z':
        S1_slice = S1[:, :, slice_index]
        S2_slice = S2[:, :, slice_index]
        S3_slice = S3[:, :, slice_index]
        x_label, y_label = 'X', 'Y'
        slice_val = Z[0, 0, slice_index]
        title = f'Hopf Soliton Slice (Z = {slice_val:.2f})'
    elif slice_axis == 'y':
        S1_slice = S1[:, slice_index, :]
        S2_slice = S2[:, slice_index, :]
        S3_slice = S3[:, slice_index, :]
        x_label, y_label = 'X', 'Z'
        slice_val = Y[0, slice_index, 0]
        title = f'Hopf Soliton Slice (Y = {slice_val:.2f})'
    else:  # slice_axis == 'x'
        S1_slice = S1[slice_index, :, :]
        S2_slice = S2[slice_index, :, :]
        S3_slice = S3[slice_index, :, :]
        x_label, y_label = 'Y', 'Z'
        slice_val = X[slice_index, 0, 0]
        title = f'Hopf Soliton Slice (X = {slice_val:.2f})'

    # Create a 2D color plot of the Stokes parameters
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    im1 = axes[0].imshow(S1_slice.T, origin='lower', extent=[-2, 2, -2, 2], cmap='viridis')
    axes[0].set_title('S1 Parameter')
    axes[0].set_xlabel(x_label)
    axes[0].set_ylabel(y_label)
    fig.colorbar(im1, ax=axes[0])

    im2 = axes[1].imshow(S2_slice.T, origin='lower', extent=[-2, 2, -2, 2], cmap='viridis')
    axes[1].set_title('S2 Parameter')
    axes[1].set_xlabel(x_label)
    axes[1].set_ylabel(y_label)
    fig.colorbar(im2, ax=axes[1])

    im3 = axes[2].imshow(S3_slice.T, origin='lower', extent=[-2, 2, -2, 2], cmap='viridis')
    axes[2].set_title('S3 Parameter')
    axes[2].set_xlabel(x_label)
    axes[2].set_ylabel(y_label)
    fig.colorbar(im3, ax=axes[2])

    fig.suptitle(title)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # --- Simulation Parameters ---
    GRID_SIZE = 100
    BEAM_WAIST = 1.0
    WAVELENGTH1 = 0.8
    WAVELENGTH2 = 1.2
    K_VAL = 1.0
    TIME = 0.0
    
    # --- Run Simulation ---
    grid, stokes_parameters = create_hopf_soliton(
        grid_size=GRID_SIZE,
        beam_waist=BEAM_WAIST,
        wavelength1=WAVELENGTH1,
        wavelength2=WAVELENGTH2,
        k_val=K_VAL,
        time=TIME
    )

    # --- Visualize Results ---
    visualize_hopf_soliton(grid, stokes_parameters, slice_axis='z')
