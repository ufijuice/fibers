import gdsfactory as gf
from microcomb import soliton_microcomb_resonator

@gf.cell
def photonic_retina(rows: int = 2, cols: int = 2, spacing: float = 100.0):
    """
    Creates a 2D array of soliton_microcomb_resonator components.

    Args:
        rows: The number of rows in the array.
        cols: The number of columns in the array.
        spacing: The spacing between the resonators in microns.
    """
    # Create a new component to hold our retina
    c = gf.Component("photonic_retina")

    # Create the array of resonators
    for row in range(rows):
        for col in range(cols):
            resonator = c << soliton_microcomb_resonator()
            resonator.move((col * spacing, row * spacing))

    return c

if __name__ == "__main__":
    # 1. Instantiate the component with default parameters
    my_photonic_retina = photonic_retina()

    # 2. Show the component in the KLayout viewer.
    print("Showing layout in KLayout...")
    my_photonic_retina.show()

    # 3. Save the layout to a GDSII file.
    gds_filename = "photonic_retina.gds"
    my_photonic_retina.write_gds(gds_filename)
    print(f"Layout saved to {gds_filename}")
