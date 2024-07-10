import numpy as np
import wave
from scipy.signal import butter, lfilter
import receiver_gui

def read(file_path):
    # Read an audio file and return its samples and frame rate
    with wave.open(file_path, 'r') as wf:
        samples = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
        frame_rate = wf.getframerate()
    return samples, frame_rate

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def demodulate(signal, sampling_rate, base_freq=1500, offset=1000):
    # Bandpass filter to mitigate noise outside the frequency range
    lowcut = base_freq - offset * 1.5
    highcut = base_freq + offset * 1.5
    filtered_signal = bandpass_filter(signal, lowcut, highcut, sampling_rate)

    # Demodulate an FSK signal to binary data
    freq0 = base_freq - offset
    freq1 = base_freq + offset

    t = np.arange(len(filtered_signal)) / sampling_rate
    analytic_signal0 = np.exp(2j * np.pi * freq0 * t) * filtered_signal
    analytic_signal1 = np.exp(2j * np.pi * freq1 * t) * filtered_signal
    
    instantaneous_phase0 = np.unwrap(np.angle(analytic_signal0))
    instantaneous_phase1 = np.unwrap(np.angle(analytic_signal1))
    
    phase_derivative0 = np.diff(instantaneous_phase0)
    phase_derivative1 = np.diff(instantaneous_phase1)
    
    # Adaptive thresholding
    mean_phase0 = np.mean(phase_derivative0)
    mean_phase1 = np.mean(phase_derivative1)
    
    binary_data = (phase_derivative1 - mean_phase1 > phase_derivative0 - mean_phase0).astype(int)
    
    bit_duration = len(filtered_signal) / len(binary_data)
    
    return binary_data, bit_duration

def convert(binary_data, sampling_rate, bit_duration):
    # Convert binary data back to audio samples
    bit_samples = int(bit_duration * sampling_rate)
    audio_samples = np.repeat(binary_data, bit_samples)
    return audio_samples

def save(signal, file_path, sampling_rate):
    # Save the signal to an audio file
    signal = (signal * 32767).astype(np.int16)  # Normalize and convert to 16-bit PCM
    with wave.open(file_path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sampling_rate)  # Use the same sampling rate to maintain duration
        wf.writeframes(signal.tobytes())

def run(input, output, base_freq, offset):
    # Main function to run the receiver
    samples, sampling_rate = read(input)
    binary_data, bit_duration = demodulate(samples, sampling_rate, base_freq, offset)
    audio_samples = convert(binary_data, sampling_rate, bit_duration)
    save(audio_samples, output, sampling_rate)
    
    return binary_data, audio_samples, sampling_rate

if __name__ == "__main__":
    receiver_gui.display(run)
