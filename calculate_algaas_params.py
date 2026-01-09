#!/usr/bin/env python3
"""
Calculate optimal simulation parameters for AlGaAs solitons.
"""
import numpy as np

# AlGaAs material properties
n0 = 3.3
n2 = 1e-17  # m²/W
beta_tpa = 1.5e-11  # m/W
wavelength = 1.55e-6  # m (or could use 0.8-1.0 µm for AlGaAs)

# Alternative wavelength common for AlGaAs
wavelength_algaas = 0.85e-6  # 850 nm (common for AlGaAs)

print("=" * 70)
print("ALGAAS SOLITON PARAMETER CALCULATOR")
print("=" * 70)

for wl, name in [(wavelength, "1.55 µm (telecom)"), (wavelength_algaas, "850 nm (AlGaAs typical)")]:
    print(f"\n--- Wavelength: {name} ---")

    k0 = 2 * np.pi / wl
    k = k0 * n0

    # Critical power for spatial soliton
    # P_crit ~ λ² / (n0 * n2) for (2+1)D spatial solitons
    P_crit = wl**2 / (n0 * n2)

    print(f"\nCritical Power for fundamental spatial soliton:")
    print(f"  P_crit = {P_crit:.2e} W = {P_crit/1000:.2f} kW")

    # For the simulation with effective_area = 1e-12 m²
    effective_area = 1e-12  # m²

    # Power options for different soliton numbers
    print(f"\nRecommended power settings (for effective_area = {effective_area:.2e} m²):")
    for N in [0.5, 1.0, 1.5, 2.0]:
        P = N**2 * P_crit
        intensity = P / effective_area
        print(f"  N={N:.1f}: Power = {P:.2e} W ({P/1000:.1f} kW), Intensity = {intensity/1e13:.2f} GW/cm²")

    # Estimate nonlinear length and diffraction length
    P_typical = P_crit  # Use N=1 for estimates
    I_typical = P_typical / effective_area
    L_NL = 1 / (k0 * n2 * I_typical)

    # For beam waist w0 ~ 1 µm
    beam_waist_physical = 1e-6  # m
    L_diff = k * beam_waist_physical**2

    print(f"\nCharacteristic lengths (for P = P_crit, w0 = {beam_waist_physical*1e6:.1f} µm):")
    print(f"  Nonlinear length L_NL = {L_NL*1e3:.3f} mm")
    print(f"  Diffraction length L_diff = {L_diff*1e3:.3f} mm")
    print(f"  Ratio L_NL/L_diff = {L_NL/L_diff:.3f}")

    # Propagation parameters
    print(f"\nSuggested simulation parameters:")
    print(f"  --wavelength {wl*1e6:.3f}e-6")
    print(f"  --power {P_crit:.2e}  (for fundamental soliton N=1)")
    print(f"  --beam-waist 1.0  (in grid units)")
    print(f"  --grid-size 64  (higher = better resolution)")

    # Calculate optimal dz step
    # Want dz << min(L_NL, L_diff) for accuracy
    # A good rule: dz ~ 0.01 * min(L_NL, L_diff)
    L_min = min(L_NL, L_diff)
    dz_physical = 0.01 * L_min
    print(f"  --dz (step size): recommend ~{dz_physical*1e6:.3f}e-6 m")
    print(f"    (In dimensionless units, use small values like 0.001-0.01)")

    # Two-photon absorption effects
    print(f"\nTwo-photon absorption effects:")
    TPA_length = 1 / (beta_tpa * I_typical)
    print(f"  TPA absorption length L_TPA = {TPA_length*1e3:.2f} mm")
    if TPA_length < 10 * L_NL:
        print(f"  ⚠️  TPA is significant! (L_TPA/L_NL = {TPA_length/L_NL:.2f})")
        print(f"     Solitons will decay due to TPA (not currently modeled)")
    else:
        print(f"  ✓ TPA is weak compared to nonlinear effects")

print("\n" + "=" * 70)
print("SIMULATION RECOMMENDATIONS FOR ALGAAS")
print("=" * 70)
print("""
For best results with collision simulations:

1. Use lower power initially to test:
   python soliton.py run collision --material algaas --power 5e4 \\
     --grid-size 64 --num-steps 100

2. For fundamental solitons (N≈1):
   python soliton.py run collision --material algaas --power 7.3e4 \\
     --grid-size 64 --num-steps 150

3. For gate simulations:
   python soliton.py run gates --material algaas --power 7.3e4 \\
     --grid-size 64 --num-steps 200

4. Adjust --angle to control collision angle (default 0.1 is reasonable)
   Smaller angle = more head-on collision

5. Two-photon absorption in AlGaAs is significant at high intensities.
   The simulation doesn't model TPA losses yet, so solitons may appear
   more stable than in reality.

Note: The 'effective_area' parameter (1e-12 m²) is somewhat arbitrary
since spatial coordinates are in dimensionless grid units. What matters
is that power/area gives the right intensity for the n2 nonlinearity.
""")
