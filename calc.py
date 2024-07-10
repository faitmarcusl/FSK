import numpy as np
import wave
from calc_gui import BER_SNR_GUI
import tkinter as tk

def calculate_ber(original_bits, demodulated_bits):
    min_len = min(len(original_bits), len(demodulated_bits))
    original_bits = original_bits[:min_len]
    demodulated_bits = demodulated_bits[:min_len]
    errors = np.sum(original_bits != demodulated_bits)
    ber = errors / min_len
    return ber

def calculate_snr(ber):
    snr_raw = 1 / (2 * ber)
    snr = 10 * np.log10(snr_raw)
    return snr

def audio_to_bitstream(file_path):
    with wave.open(file_path, 'rb') as wf:
        frames = wf.readframes(wf.getnframes())
        bitstream = np.unpackbits(np.frombuffer(frames, dtype=np.uint8))
    return bitstream

def audio_to_signal(file_path):
    with wave.open(file_path, 'rb') as wf:
        frames = wf.readframes(wf.getnframes())
        signal = np.frombuffer(frames, dtype=np.int16)
    return signal

def calculate_metrics(original_file, demodulated_file):
    original_bits = audio_to_bitstream(original_file)
    demodulated_bits = audio_to_bitstream(demodulated_file)
    
    ber = calculate_ber(original_bits, demodulated_bits)    
    snr = calculate_snr(ber)
    
    
    return ber, snr

# GUI setup
root = tk.Tk()
gui = BER_SNR_GUI(root, calculate_metrics)
root.mainloop()