import numpy as np
import matplotlib.pyplot as plt

def create_hopfion_crystal(p_val, q_val, lattice_type='sc', size=1.0, resolution=100, lattice_constant=1.0):
    """
    Creates a hopfion crystal.

    Args:
        p_val (int): The p-value for the rational map.
        q_val (int): The q-value for the rational map.
        lattice_type (str): The type of crystal lattice ('sc', 'bcc', 'fcc').
        size (float): The size of the simulation box.
        resolution (int): The resolution of the grid.
        lattice_constant (float): The lattice constant 'a'.

    Returns:
        tuple: A tuple containing the grid coordinates (X, Y, Z) and the spin texture (S1, S2, S3).
    """
    # Create a grid of points
    x = np.linspace(-size, size, resolution)
    y = np.linspace(-size, size, resolution)
    z = np.linspace(-size, size, resolution)
    X, Y, Z = np.meshgrid(x, y, z)

    print(f"Generating a {lattice_type} hopfion crystal with p={p_val}, q={q_val}")

    k = 2 * np.pi / lattice_constant

    # Define intermediate complex fields based on lattice type
    if lattice_type == 'sc':
        # Wave vectors for simple cubic
        kx = k * X
        ky = k * Y
        # Intermediate fields for simple cubic
        Z0_base = np.cos(kx) + 1j * np.sin(kx)
        Z1_base = np.cos(ky) + 1j * np.sin(ky)

    elif lattice_type == 'bcc':
        # Wave vectors for body-centered cubic
        k1 = k * (Y + Z)
        k2 = k * (X + Z)
        # Intermediate fields for body-centered cubic
        Z0_base = np.cos(k1) + 1j * np.sin(k1)
        Z1_base = np.cos(k2) + 1j * np.sin(k2)

    elif lattice_type == 'fcc':
        # Wave vectors for face-centered cubic
        k1 = k * (X + Y - Z)
        k2 = k * (X - Y + Z)
        # Intermediate fields for face-centered cubic
        Z0_base = np.cos(k1) + 1j * np.sin(k1)
        Z1_base = np.cos(k2) + 1j * np.sin(k2)

    else:
        print(f"Lattice type '{lattice_type}' is not yet implemented.")
        # Return a uniform spin texture
        S1 = np.zeros_like(X)
        S2 = np.zeros_like(X)
        S3 = np.ones_like(X)
        return (X, Y, Z), (S1, S2, S3)

    # Apply the rational map powers
    Z0 = Z0_base ** q_val
    Z1 = Z1_base ** p_val

    # Normalize the complex fields
    norm = np.sqrt(np.abs(Z0)**2 + np.abs(Z1)**2)
    # Avoid division by zero
    norm[norm == 0] = 1
    Z0 /= norm
    Z1 /= norm

    # Calculate the spin texture from the normalized complex fields
    # S_x = 2 * Re(Z1 * conj(Z0))
    # S_y = 2 * Im(Z1 * conj(Z0))
    # S_z = |Z0|^2 - |Z1|^2
    S1 = 2 * (Z1.real * Z0.real + Z1.imag * Z0.imag)
    S2 = 2 * (Z1.imag * Z0.real - Z1.real * Z0.imag)
    S3 = np.abs(Z0)**2 - np.abs(Z1)**2

    return (X, Y, Z), (S1, S2, S3)

def visualize_hopfion_crystal(grid, spin_texture, slice_axis='z', slice_index=None):
    """
    Visualizes a slice of the hopfion crystal.

    Args:
        grid (tuple): The grid coordinates (X, Y, Z).
        spin_texture (tuple): The spin texture (S1, S2, S3).
        slice_axis (str): The axis to slice along ('x', 'y', or 'z').
        slice_index (int): The index of the slice. If None, the middle slice is used.
    """
    X, Y, Z = grid
    S1, S2, S3 = spin_texture

    if slice_index is None:
        slice_index = S1.shape[0] // 2

    if slice_axis == 'z':
        S1_slice = S1[:, :, slice_index]
        S2_slice = S2[:, :, slice_index]
        S3_slice = S3[:, :, slice_index]
        x_label, y_label = 'X', 'Y'
        slice_val = Z[0, 0, slice_index]
        title = f'Hopfion Crystal Slice (Z = {slice_val:.2f})'
    elif slice_axis == 'y':
        S1_slice = S1[:, slice_index, :]
        S2_slice = S2[:, slice_index, :]
        S3_slice = S3[:, slice_index, :]
        x_label, y_label = 'X', 'Z'
        slice_val = Y[0, slice_index, 0]
        title = f'Hopfion Crystal Slice (Y = {slice_val:.2f})'
    else:  # slice_axis == 'x'
        S1_slice = S1[slice_index, :, :]
        S2_slice = S2[slice_index, :, :]
        S3_slice = S3[slice_index, :, :]
        x_label, y_label = 'Y', 'Z'
        slice_val = X[slice_index, 0, 0]
        title = f'Hopfion Crystal Slice (X = {slice_val:.2f})'

    # Create a 2D color plot of the spin components
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    im1 = axes[0].imshow(S1_slice.T, origin='lower', extent=[-1, 1, -1, 1], cmap='viridis')
    axes[0].set_title('S1 Component')
    axes[0].set_xlabel(x_label)
    axes[0].set_ylabel(y_label)
    fig.colorbar(im1, ax=axes[0])

    im2 = axes[1].imshow(S2_slice.T, origin='lower', extent=[-1, 1, -1, 1], cmap='viridis')
    axes[1].set_title('S2 Component')
    axes[1].set_xlabel(x_label)
    axes[1].set_ylabel(y_label)
    fig.colorbar(im2, ax=axes[1])

    im3 = axes[2].imshow(S3_slice.T, origin='lower', extent=[-1, 1, -1, 1], cmap='viridis')
    axes[2].set_title('S3 Component')
    axes[2].set_xlabel(x_label)
    axes[2].set_ylabel(y_label)
    fig.colorbar(im3, ax=axes[2])

    fig.suptitle(title)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # --- Simulation Parameters ---
    P_VALUE = 1
    Q_VALUE = 1
    LATTICE_TYPE = 'fcc'  # 'sc', 'bcc', or 'fcc'
    SIMULATION_SIZE = 2.0 # Increased size to see more of the crystal
    GRID_RESOLUTION = 50
    LATTICE_CONSTANT = 1.0
    
    # --- Run Simulation ---
    grid, spin_texture = create_hopfion_crystal(
        p_val=P_VALUE,
        q_val=Q_VALUE,
        lattice_type=LATTICE_TYPE,
        size=SIMULATION_SIZE,
        resolution=GRID_RESOLUTION,
        lattice_constant=LATTICE_CONSTANT
    )

    # --- Visualize Results ---
    visualize_hopfion_crystal(grid, spin_texture, slice_axis='z')
