import numpy as np
import wave
import tkinter as tk
from tkinter import filedialog, messagebox
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def add_rayleigh_fading(signal):
    """
    Rayleigh Fading Channel
    """
    rayleigh_noise = np.sqrt(0.5) * (np.random.normal(size=signal.shape) + 1j * np.random.normal(size=signal.shape))
    faded_signal = signal * rayleigh_noise
    return np.real(faded_signal)

def process_audio(file_path, output_path):
    # Read the audio file
    with wave.open(file_path, 'rb') as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        audio_data = wf.readframes(n_frames)
    
    audio_signal = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)

    # Normalize the signal
    max_val = np.max(np.abs(audio_signal))
    audio_signal /= max_val

    # Apply Rayleigh fading
    faded_signal = add_rayleigh_fading(audio_signal)

    # Denormalize the signal
    faded_signal *= max_val
    faded_signal = faded_signal.astype(np.int16)

    # Write the processed audio to a new file
    write(output_path, framerate, faded_signal)

    return audio_signal, faded_signal

def find_and_plot(signal, faded_signal, framerate):
    # Find the first instance of bit 1 and take the next 1000 samples
    threshold = 0.5 * np.max(signal)
    start_idx = np.where(signal > threshold)[0][0]
    end_idx = start_idx + 1000

    if end_idx > len(signal):
        end_idx = len(signal)
    
    segment_orig = signal[start_idx:end_idx]
    segment_faded = faded_signal[start_idx:end_idx]

    time = np.arange(0, len(segment_orig)) / framerate

    fig, axs = plt.subplots(2, 1, figsize=(10, 6))

    axs[0].plot(time, segment_orig)
    axs[0].set_title('Original Signal Segment')
    axs[0].set_xlabel('Time [s]')
    axs[0].set_ylabel('Amplitude')

    axs[1].plot(time, segment_faded)
    axs[1].set_title('Rayleigh Faded Signal Segment')
    axs[1].set_xlabel('Time [s]')
    axs[1].set_ylabel('Amplitude')

    plt.tight_layout()
    return fig

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if file_path:
        output_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
        if output_path:
            original_signal, faded_signal = process_audio(file_path, output_path)
            fig = find_and_plot(original_signal, faded_signal, 44100)

            canvas = FigureCanvasTkAgg(fig, master=root)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)
            messagebox.showinfo("Success", f"Processed file saved to {output_path}")

# Tkinter GUI
root = tk.Tk()
root.title("Rayleigh Fading Simulation")

tk.Label(root, text="Rayleigh Fading Simulation").pack(pady=10)
tk.Button(root, text="Open Audio File", command=open_file).pack(pady=20)

root.mainloop()