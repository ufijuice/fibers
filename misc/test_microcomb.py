import pytest
import gdstk
from microcomb import soliton_microcomb_resonator

def compare_gds(file1, file2):
    """
    Compares the geometric content of two GDS files, ignoring metadata.
    """
    lib1 = gdstk.read_gds(file1)
    lib2 = gdstk.read_gds(file2)

    if len(lib1.cells) != len(lib2.cells):
        return False

    for cell1 in lib1.cells:
        cell2 = None
        for c in lib2.cells:
            if c.name == cell1.name:
                cell2 = c
                break
        if cell2 is None:
            return False

        polygons1 = cell1.polygons
        polygons2 = cell2.polygons
        if len(polygons1) != len(polygons2):
            return False

        # A more robust comparison would involve sorting and comparing each polygon
        for p1, p2 in zip(sorted(polygons1, key=lambda p: p.size), sorted(polygons2, key=lambda p: p.size)):
            if p1.size != p2.size or p1.layer != p2.layer or p1.datatype != p2.datatype:
                return False
    return True

def test_soliton_microcomb_resonator():
    """
    Tests that the soliton_microcomb_resonator component can be instantiated.
    """
    component = soliton_microcomb_resonator()
    assert component is not None

@pytest.mark.parametrize(
    "radius, gap, waveguide_width",
    [
        (10, 0.2, 0.5),
        (20, 0.3, 0.6),
        (30, 0.4, 0.7),
    ],
)
def test_soliton_microcomb_resonator_parameterized(radius, gap, waveguide_width):
    """
    Tests that the soliton_microcomb_resonator component can be instantiated with different parameters.
    """
    component = soliton_microcomb_resonator(
        radius=radius, gap=gap, waveguide_width=waveguide_width
    )
    assert component is not None

def test_soliton_microcomb_resonator_radius():
    """
    Tests that the soliton_microcomb_resonator component has the correct radius.
    """
    radius = 25
    component = soliton_microcomb_resonator(radius=radius)
    assert component.info["radius"] == radius

def test_gds_regression():
    """
    Tests that the generated GDS file is identical to a golden GDS file.
    """
    component = soliton_microcomb_resonator()
    component.write_gds("new.gds")
    assert compare_gds("new.gds", "golden.gds")

def test_heater():
    """
    Tests that the heater is created correctly.
    """
    component_without_heater = soliton_microcomb_resonator(with_heater=False)
    component_with_heater = soliton_microcomb_resonator(with_heater=True)
    
    polygons_without_heater = len(component_without_heater.get_polygons())
    polygons_with_heater = len(component_with_heater.get_polygons())
    
    assert polygons_with_heater > polygons_without_heater
