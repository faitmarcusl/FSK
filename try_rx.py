import numpy as np
import wave
import receiver_gui

def read(file_path):
    # Read an audio file and return its samples and frame rate
    with wave.open(file_path, 'r') as wf:
        samples = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
        frame_rate = wf.getframerate()
    return samples, frame_rate

def demodulate(signal, sampling_rate, base_freq=1500, offset=1000):
    # Demodulate an FSK signal to binary data
    freq0 = base_freq - offset
    freq1 = base_freq + offset

    t = np.arange(len(signal)) / sampling_rate
    analytic_signal = np.exp(2j * np.pi * (freq0 * t)) * signal + np.exp(2j * np.pi * (freq1 * t)) * signal
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    phase_derivative = np.diff(instantaneous_phase)
    
    bit_duration = len(signal) / len(phase_derivative)
    threshold = np.median(phase_derivative)
    binary_data = (phase_derivative > threshold).astype(int)
    
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
