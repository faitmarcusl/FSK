import numpy as np
from scipy.signal import hilbert, welch
from pydub import AudioSegment
import wave
from rx_gui import display  # Import only the display function
 
def read_fsk(file_path):
    with wave.open(file_path, 'r') as wf:
        frames = wf.readframes(wf.getnframes())
        samples = np.frombuffer(frames, dtype=np.int16) / 32767.0  # Normalize
        sampling_rate = wf.getframerate()
    return samples, sampling_rate

def demodulate(signal, sampling_rate, base_freq=1500, offset=1000):
    freq0 = base_freq - offset
    freq1 = base_freq + offset

    analytic_signal = hilbert(signal)
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    instantaneous_frequency = np.diff(instantaneous_phase) * sampling_rate / (2.0 * np.pi)

    threshold = (freq0 + freq1) / 2
    binary_data = (instantaneous_frequency > threshold).astype(int)

    return binary_data, instantaneous_frequency

def save_audio(binary_data, file_path, sampling_rate):
    samples = (binary_data * 2 - 1) * 32767
    samples = samples.astype(np.int16)
    
    audio = AudioSegment(
        samples.tobytes(),
        frame_rate=sampling_rate,
        sample_width=samples.dtype.itemsize,
        channels=1
    )
    audio.export(file_path, format="wav")

def run_reverse(input_path, output_path, base_freq, offset):
    fsk_signal, sampling_rate = read_fsk(input_path)
    binary_data, instantaneous_frequency = demodulate(fsk_signal, sampling_rate, base_freq, offset)
    save_audio(binary_data, output_path, sampling_rate)

    return fsk_signal, sampling_rate, instantaneous_frequency

if __name__ == "__main__":
    display(run_reverse)
