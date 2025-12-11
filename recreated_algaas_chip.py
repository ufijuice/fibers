import numpy as np
import matplotlib.pyplot as plt
import time

"""
This script simulates the behavior of the AlGaAs microresonator array for
entanglement generation, as described in the paper PRX Quantum 6, 010338 (2025).

Simulation vs. Real Hardware Speed:

This simulation calculates the expected transmission spectrum and Joint Spectral
Intensity (JSI) of the device. The "speed" of this simulation is the time it
takes for the script to run, which depends on the simulation parameters (e.g.,
grid size) and the computer's performance.

The "speed" of the real hardware refers to the rate at which it can generate
entangled photon pairs. The paper reports a pair-generation rate of up to
2.6 GHz/mW^2. This means that for every milliwatt squared of pump power, the
device can generate 2.6 billion entangled photon pairs per second.

There is no direct comparison between the simulation speed and the hardware
speed, as they represent fundamentally different processes. The simulation
predicts the outcome, while the hardware performs the physical process.
"""

def get_resonator_spectrum(freqs, center_freq, fwhm, depth):
    """
    Calculates the transmission spectrum of a single resonator.

    Args:
        freqs (np.ndarray): Array of frequencies to calculate the spectrum for.
        center_freq (float): Center frequency of the resonance.
        fwhm (float): Full width at half maximum of the resonance.
        depth (float): Depth of the resonance in dB.

    Returns:
        np.ndarray: The transmission spectrum in dB.
    """
    return -depth / (1 + ((freqs - center_freq) / (fwhm / 2))**2)

def simulate_resonator_array(num_resonators=5, fsr=650e9, q_factor=3.5e5, center_wavelength=1560e-9, detuning_ghz=12.5e9):
    """
    Simulates the transmission spectrum of an array of microresonators.

    Args:
        num_resonators (int): The number of resonators in the array.
        fsr (float): The free spectral range of the resonators in Hz.
        q_factor (float): The quality factor of the resonators.
        center_wavelength (float): The center wavelength of the pump laser in meters.
        detuning_ghz (float): The detuning between adjacent resonators in Hz.

    Returns:
        tuple: A tuple containing the frequency array and the total transmission spectrum.
    """
    c = 299792458  # Speed of light in m/s
    center_freq = c / center_wavelength
    fwhm = center_freq / q_factor

    # Frequency range for plotting
    freq_span = fsr * 1.5
    freqs = np.linspace(center_freq - freq_span / 2, center_freq + freq_span / 2, 2000)

    total_transmission = np.zeros_like(freqs)

    for i in range(num_resonators):
        resonator_center_freq = center_freq + (i - (num_resonators - 1) / 2) * detuning_ghz
        total_transmission += get_resonator_spectrum(freqs, resonator_center_freq, fwhm, depth=10)

    return freqs, total_transmission

def visualize_spectrum(freqs, transmission, center_wavelength=1560e-9):
    """
    Visualizes the transmission spectrum.

    Args:
        freqs (np.ndarray): The frequency array.
        transmission (np.ndarray): The transmission spectrum.
        center_wavelength (float): The center wavelength for labeling.
    """
    c = 299792458
    center_freq = c / center_wavelength
    
    plt.figure(figsize=(10, 6))
    plt.plot((freqs - center_freq) * 1e-9, transmission)
    plt.xlabel("Frequency Detuning (GHz)")
    plt.ylabel("Transmission (dB)")
    plt.title("Microresonator Array Transmission Spectrum")
    plt.grid(True)
    plt.show()

def simulate_sfwm_and_jsi(num_resonators=5, fsr=650e9, q_factor=3.5e5, center_wavelength=1560e-9, detuning_ghz=12.5e9):
    """
    Simulates the SFWM process and calculates the Joint Spectral Intensity (JSI).

    Args:
        num_resonators (int): The number of resonators in the array.
        fsr (float): The free spectral range of the resonators in Hz.
        q_factor (float): The quality factor of the resonators.
        center_wavelength (float): The center wavelength of the pump laser in meters.
        detuning_ghz (float): The detuning between adjacent resonators in Hz.
    """
    c = 299792458
    center_freq = c / center_wavelength
    fwhm = center_freq / q_factor

    # Frequencies for signal and idler
    freq_span = fsr * 1.5
    freqs = np.linspace(center_freq - freq_span, center_freq + freq_span, 200)
    signal_freqs, idler_freqs = np.meshgrid(freqs, freqs)

    jsi = np.zeros_like(signal_freqs)

    for i in range(num_resonators):
        pump_freq = center_freq + (i - (num_resonators - 1) / 2) * detuning_ghz
        
        # Phase matching condition: 2 * pump = signal + idler
        phase_matching = np.exp(-((2 * pump_freq - signal_freqs - idler_freqs) / (fwhm))**2)
        
        # Resonator enhancement
        signal_enhancement = 1 / (1 + ((signal_freqs - pump_freq - fsr) / (fwhm / 2))**2)
        idler_enhancement = 1 / (1 + ((idler_freqs - pump_freq + fsr) / (fwhm / 2))**2)
        
        jsi += phase_matching * signal_enhancement * idler_enhancement

    return freqs, freqs, jsi

def visualize_jsi(signal_freqs, idler_freqs, jsi, center_wavelength=1560e-9):
    """
    Visualizes the Joint Spectral Intensity (JSI).

    Args:
        signal_freqs (np.ndarray): The signal frequency array.
        idler_freqs (np.ndarray): The idler frequency array.
        jsi (np.ndarray): The JSI matrix.
        center_wavelength (float): The center wavelength for labeling.
    """
    c = 299792458
    center_freq = c / center_wavelength

    plt.figure(figsize=(8, 8))
    plt.imshow(jsi, extent=[(signal_freqs[0] - center_freq) * 1e-9, (signal_freqs[-1] - center_freq) * 1e-9,
                             (idler_freqs[0] - center_freq) * 1e-9, (idler_freqs[-1] - center_freq) * 1e-9],
               origin='lower', cmap='viridis')
    plt.xlabel("Signal Frequency Detuning (GHz)")
    plt.ylabel("Idler Frequency Detuning (GHz)")
    plt.title("Joint Spectral Intensity (JSI)")
    plt.colorbar(label="Intensity (arb. units)")
    plt.show()


if __name__ == '__main__':
    start_time = time.time()

    # Parameters from the paper
    NUM_RESONATORS = 5
    FSR = 650e9  # Hz
    Q_FACTOR = 3.5e5
    CENTER_WAVELENGTH = 1560.18e-9 # meters, from Fig 2(e)
    DETUNING = 12.5e9 # Hz

    # --- Simulate the resonator array ---
    print("Simulating the resonator array...")
    freqs, transmission = simulate_resonator_array(
        num_resonators=NUM_RESONATORS,
        fsr=FSR,
        q_factor=Q_FACTOR,
        center_wavelength=CENTER_WAVELENGTH,
        detuning_ghz=DETUNING
    )

    # --- Visualize the spectrum ---
    visualize_spectrum(freqs, transmission, center_wavelength=CENTER_WAVELENGTH)

    # --- Simulate SFWM and JSI ---
    print("Simulating SFWM and JSI...")
    signal_freqs, idler_freqs, jsi = simulate_sfwm_and_jsi(
        num_resonators=NUM_RESONATORS,
        fsr=FSR,
        q_factor=Q_FACTOR,
        center_wavelength=CENTER_WAVELENGTH,
        detuning_ghz=DETUNING
    )

    # --- Visualize the JSI ---
    visualize_jsi(signal_freqs, idler_freqs, jsi, center_wavelength=CENTER_WAVELENGTH)
    
    end_time = time.time()
    simulation_time = end_time - start_time
    print(f"Simulation finished in {simulation_time:.2f} seconds.")

    # --- Hardware Time Comparison ---
    # The paper reports a pair-generation efficiency of 2.6 GHz/mW^2.
    # Assuming a pump power of 1 mW, the rate is 2.6e9 pairs/second.
    # We can calculate the time it would take for the hardware to generate
    # a certain number of pairs.
    generation_rate = 2.6e9  # pairs per second
    num_pairs_to_generate = 1_000_000
    hw_time = num_pairs_to_generate / generation_rate
    
    print(f"Equivalent hardware time to generate {num_pairs_to_generate} pairs: {hw_time:.6f} seconds.")
