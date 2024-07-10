import tkinter as tk
from tkinter import filedialog, messagebox
import ber_snr_gui as gui

import numpy as np
import wave

def read_audio(file_path):
    with wave.open(file_path, 'r') as wf:
        samples = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
        frame_rate = wf.getframerate()
    return samples, frame_rate

def extract_binary_data(samples):
    binary_data = (samples > np.median(samples)).astype(int)
    return binary_data

def calculate_ber(original_data, demodulated_data):
    bit_errors = np.sum(original_data != demodulated_data)
    total_bits = len(original_data)
    ber = bit_errors / total_bits
    return ber

def calculate_snr(modulated_signal, demodulated_signal):
    signal_power = np.mean(modulated_signal**2)
    noise_power = np.mean((modulated_signal - demodulated_signal)**2)
    snr = 10 * np.log10(signal_power / noise_power)
    return snr

def calculate_ber_snr(original_file, modulated_file, demodulated_file, environment):
    original_samples, original_rate = read_audio(original_file)
    modulated_samples, modulated_rate = read_audio(modulated_file)
    demodulated_samples, demodulated_rate = read_audio(demodulated_file)

    assert original_rate == modulated_rate == demodulated_rate, "Sampling rates must match."

    original_data = extract_binary_data(original_samples)
    demodulated_data = extract_binary_data(demodulated_samples)

    ber = calculate_ber(original_data, demodulated_data)
    snr = calculate_snr(modulated_samples, demodulated_samples)

    return ber, snr

if __name__ == "__main__":
    root = tk.Tk()
    app = gui.BER_SNR_Calculator_GUI(root)
    root.mainloop()
