import numpy as np
import matplotlib.pyplot as plt
import click
import os
import time

# --- Simulation Core ---

def create_gaussian_pulse(t, power, width):
    """Creates a Gaussian pulse centered at t=0."""
    return power * np.exp(-t**2 / (2 * width**2))

def apply_loss(initial_power, distance, alpha):
    """
    Calculates the attenuated power after propagation.
    alpha is loss in dB/km.
    """
    linear_loss = 10**(-alpha / 10)
    final_power = initial_power * (linear_loss**distance)
    return final_power

def apply_dispersion(initial_width, distance, beta2, wavelength):
    """
    Calculates the pulse width after dispersive broadening.
    beta2 is the GVD parameter in ps^2/km.
    wavelength is in nm.
    """
    # Formula for Gaussian pulse broadening: width_out^2 = width_in^2 + (beta2 * L / width_in)^2
    # A more complete model would involve Fourier transforms, but for simple
    # Gaussian pulses, this analytical approach is fast and illustrative.
    if initial_width < 1e-9: # Avoid division by zero
        return initial_width
    
    # Convert beta2 from ps^2/km to s^2/m
    beta2_si = beta2 * (1e-12)**2 / 1e3

    # Convert distance from km to m
    distance_m = distance * 1e3

    # Calculate broadened width
    width_out_sq = initial_width**2 + (beta2_si * distance_m / initial_width)**2
    return np.sqrt(width_out_sq)

def simulate_transmission(params):
    """
    Runs the system-level simulation for many pulses to gather statistics.
    """
    t = np.linspace(-5 * params['initial_width'] * 10, 5 * params['initial_width'] * 10, params['time_resolution'])
    
    # --- Simulate a single pulse for visualization ---
    # Initial pulse
    initial_pulse = create_gaussian_pulse(t, params['initial_power'], params['initial_width'])
    
    # After loss
    power_after_loss = apply_loss(params['initial_power'], params['distance'], params['loss'])
    
    # After dispersion
    width_after_dispersion = apply_dispersion(params['initial_width'], params['distance'], params['dispersion'], params['wavelength'])
    
    # Create a representative degraded pulse for plotting
    degraded_pulse_no_jitter = create_gaussian_pulse(t, power_after_loss, width_after_dispersion)

    # --- Simulate many pulses for statistics ---
    arrival_times = []
    received_pulses = []

    click.echo(f"Simulating {params['num_pulses']} pulses...")
    for _ in range(params['num_pulses']):
        # 1. Apply jitter
        time_jitter = np.random.normal(0, params['jitter'])
        
        # 2. Add amplitude noise (as a fraction of peak power)
        amplitude_noise = np.random.normal(0, params['amplitude_noise_std'] * power_after_loss)
        
        # 3. Create the final received pulse
        received_power = power_after_loss + amplitude_noise
        if received_power < 0: received_power = 0
        
        final_pulse = create_gaussian_pulse(t - time_jitter, received_power, width_after_dispersion)
        received_pulses.append(final_pulse)
        
        # 4. Simulate detection
        # Find when the pulse crosses the comparator threshold.
        # Add random noise to the threshold itself to model comparator error.
        threshold_noise = np.random.normal(0, params['comparator_noise_std'] * params['threshold'])
        effective_threshold = params['threshold'] + threshold_noise

        # Find indices where the pulse is above threshold
        above_threshold_indices = np.where(final_pulse > effective_threshold)[0]
        
        if len(above_threshold_indices) > 0:
            # The arrival time is the *first* time it crosses the threshold
            arrival_time = t[above_threshold_indices[0]]
            arrival_times.append(arrival_time)
        else:
            # Pulse was missed (too much loss or noise)
            arrival_times.append(np.nan)
            
    click.echo("Simulation complete.")
    
    results = {
        't': t,
        'initial_pulse': initial_pulse,
        'degraded_pulse_example': degraded_pulse_no_jitter,
        'received_pulses': received_pulses,
        'arrival_times': np.array(arrival_times)
    }
    return results

# --- Visualization ---

def create_summary_plot(results, params, output_filename):
    """
    Creates a summary plot with three panels:
    1. Pulse shape comparison
    2. Arrival time histogram (jitter)
    3. Eye diagram
    """
    click.echo("Generating summary plot...")
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    fig.suptitle(f"Pulse Degradation Analysis over {params['distance']} km", fontsize=16)

    t = results['t']
    
    # --- 1. Pulse Shape Comparison ---
    ax1 = axes[0]
    ax1.plot(t / 1e-12, results['initial_pulse'], label='Initial Pulse', lw=2)
    ax1.plot(t / 1e-12, results['degraded_pulse_example'], label='Degraded Pulse (Loss & Dispersion)', ls='--', lw=2)
    # Plot a few noisy examples
    for i in range(min(5, len(results['received_pulses']))):
        ax1.plot(t / 1e-12, results['received_pulses'][i], c='gray', alpha=0.5)
    ax1.axhline(params['threshold'], color='r', ls=':', label=f"Threshold ({params['threshold']:.2f} W)")
    ax1.set_title("Pulse Shape Degradation")
    ax1.set_xlabel("Time (ps)")
    ax1.set_ylabel("Power (W)")
    ax1.legend()
    ax1.grid(True)

    # --- 2. Arrival Time Histogram ---
    ax2 = axes[1]
    valid_arrival_times = results['arrival_times'][~np.isnan(results['arrival_times'])]
    if len(valid_arrival_times) > 0:
        ax2.hist(valid_arrival_times / 1e-12, bins=50, density=True)
        total_jitter_std = np.std(valid_arrival_times)
        ax2.set_title(f"Arrival Time Jitter (Std Dev: {total_jitter_std*1e12:.2f} ps)")
    else:
        ax2.set_title("Arrival Time Jitter (No pulses detected)")
    ax2.set_xlabel("Detected Arrival Time (ps)")
    ax2.set_ylabel("Probability Density")
    ax2.grid(True)

    # --- 3. Eye Diagram ---
    ax3 = axes[2]
    # Define a time window for the eye diagram around t=0
    eye_window = params['initial_width'] * 4
    time_indices_for_eye = (t > -eye_window) & (t < eye_window)
    t_eye = t[time_indices_for_eye]
    
    for pulse in results['received_pulses']:
        ax3.plot(t_eye / 1e-12, pulse[time_indices_for_eye], color='blue', alpha=0.1)
    
    ax3.axhline(params['threshold'], color='r', ls=':', lw=1)
    ax3.set_title("Eye Diagram")
    ax3.set_xlabel("Time (ps)")
    ax3.set_ylabel("Power (W)")
    ax3.grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(output_filename, dpi=150)
    click.echo(f"Summary plot saved to {output_filename}")
    plt.close(fig)


# --- CLI ---

@click.command()
@click.option('--distance', default=50.0, help='Fiber length in km.')
@click.option('--loss', default=0.2, help='Fiber loss in dB/km.')
@click.option('--dispersion', default=17.0, help='Group Velocity Dispersion (GVD) in ps^2/km.')
@click.option('--jitter', default=5e-12, help='Intrinsic random arrival time jitter (std dev) in seconds.')
@click.option('--initial-power', default=1.0, help='Initial peak power of the pulse in W.')
@click.option('--initial-width', default=10e-12, help='Initial width (std dev) of the Gaussian pulse in seconds.')
@click.option('--threshold', default=0.1, help='Detector power threshold in W.')
@click.option('--num-pulses', default=500, help='Number of pulses to simulate for statistics.')
@click.option('--output-dir', default='results', type=click.Path())
def run(distance, loss, dispersion, jitter, initial_power, initial_width, threshold, num_pulses, output_dir):
    """
    Simulates pulse degradation due to loss, dispersion, and jitter.
    """
    params = {
        'distance': distance,
        'loss': loss,
        'dispersion': dispersion,
        'jitter': jitter,
        'initial_power': initial_power,
        'initial_width': initial_width,
        'threshold': threshold,
        'num_pulses': num_pulses,
        # Hardcoded system parameters
        'wavelength': 1550.0, # nm
        'time_resolution': 1000, # points
        'amplitude_noise_std': 0.05, # 5% of peak power
        'comparator_noise_std': 0.05, # 5% of threshold
    }

    # Run the simulation
    results = simulate_transmission(params)

    # Create visualizations
    os.makedirs(output_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename_base = f"pulse_degradation_D{distance}km_L{loss}dB_B{dispersion}ps2_{timestamp}"
    output_filename = os.path.join(output_dir, f"{filename_base}.png")
    
    create_summary_plot(results, params, output_filename)

if __name__ == '__main__':
    run()