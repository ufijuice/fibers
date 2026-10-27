import gdsfactory as gf

gf.gpdk.PDK.activate()

@gf.cell
def soliton_microcomb_resonator(radius: float = 20, gap: float = 0.2, waveguide_width: float = 0.5, with_heater: bool = False):
    """
    Creates a single-bus ring resonator, a key component for soliton microcombs.

    Args:
        radius: The radius of the ring in microns.
        gap: The coupling gap between the bus waveguide and the ring in microns.
        waveguide_width: The width of the bus and ring waveguides in microns.
        with_heater: Whether to include a heater or not.
    """
    # Create a new component to hold our ring resonator
    c = gf.Component("microcomb_resonator")

    # Use gdsfactory's built-in single-bus ring component.
    # This is much easier than creating a ring and a waveguide from scratch.
    ring_ref = c << gf.components.ring_single(
        radius=radius,
        gap=gap,
        cross_section=gf.cross_section.strip(width=waveguide_width),
        length_x=4,  # Length of the straight section of the bus waveguide
    )
    if with_heater:
        ring_cell = ring_ref.cell
        points = []
        for inst in ring_cell.insts:
            if "bend" in inst.cell.name or "straight" in inst.cell.name:
                for port in inst.ports:
                    points.append(port.center)
        
        # Remove duplicates and sort the points
        points = sorted(list(set(points)), key=lambda p: (p[0], p[1]))
        
        # Create a path from the points
        path = gf.Path(points)
        
        # Create a heater cross-section
        heater_cross_section = gf.cross_section.strip_heater_metal(width=2.0)
        
        # Extrude the path with the heater cross-section
        heater = path.extrude(cross_section=heater_cross_section)
        
        # Add electrical pads to the heater
        heater_with_pads = gf.routing.add_electrical_pads_top(heater)
        c << heater_with_pads
    
    # Add the ports from the bus waveguide to our new component so we can connect to it
    c.add_ports(ring_ref.ports)

    # Add some metadata to the component
    c.info['radius'] = radius
    c.info['gap'] = gap
    c.info['waveguide_width'] = waveguide_width

    return c

if __name__ == "__main__":
    # 1. Instantiate the component with default parameters
    my_microcomb_resonator = soliton_microcomb_resonator()

    # 2. Show the component in the KLayout viewer.
    #    This requires KLayout to be installed and configured.
    #    The viewer will open in a separate window.
    print("Showing layout in KLayout...")
    my_microcomb_resonator.show()

    # 3. Save the layout to a GDSII file.
    #    This file can be sent to a foundry for fabrication.
    gds_filename = "microcomb.gds"
    my_microcomb_resonator.write_gds(gds_filename)
    print(f"Layout saved to {gds_filename}")

    # You can also create a version with different parameters
    # large_ring = soliton_microcomb_resonator(radius=50, gap=0.15)
    # large_ring.show()
    # large_ring.write_gds("large_microcomb.gds")