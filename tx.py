import numpy as np
from pydub import AudioSegment
from pydub.utils import which
import wave
import tx_gui
 
# Configure pydub to use ffmpeg
AudioSegment.converter = which("ffmpeg")

def read(file_path):
    # Read an audio file and return its samples and frame rate
    audio = AudioSegment.from_file(file_path)
    samples = np.array(audio.get_array_of_samples())
    return samples, audio.frame_rate

def convert(data, sampling_rate, base_freq=1500, offset=1000):
    # Convert binary data to an FSK modulated signal
    freq0 = base_freq - offset  # Use user-specified offset
    freq1 = base_freq + offset  # Use user-specified offset

    # Calculate the cumulative phase based on the binary data
    phase = np.cumsum(2 * np.pi * (freq0 + (freq1 - freq0) * data) / sampling_rate)
    signal = np.sin(phase)
    return signal

def save(signal, file_path, sampling_rate):
    # Save the signal to an audio file
    signal = (signal * 32767).astype(np.int16)  # Normalize and convert to 16-bit PCM
    with wave.open(file_path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(2 * sampling_rate)  # Double the sampling rate to maintain duration
        wf.writeframes(signal.tobytes())

def run(input, output, base_freq, offset):
    # Main function to run the transmitter
    samples, sampling_rate = read(input)
    binary_data = (samples > np.median(samples)).astype(int)  # Convert audio samples to binary data using thresholding
    modulated_signal = convert(binary_data, sampling_rate, base_freq, offset)
    save(modulated_signal, output, sampling_rate)
    
    return binary_data, modulated_signal, sampling_rate

if __name__ == "__main__":
    tx_gui.display(run)
