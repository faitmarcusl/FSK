import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import soundfile as sf
from matplotlib.figure import Figure
import os
import time 

def browse(in_file):
    # Open file dialog to select an audio file
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.flac")])
    if file_path:
        in_file.set(file_path)

def start(in_file, base_freq, offset, run, progress, orig_plot, fsk_plot):
    # Start the FSK transmission process
    audio = in_file.get()
    # Create a unique output file path
    timestamp = int(time.time())
    output = f'C:/Users/Jerwin_JIL/Downloads/FSK-F/modulated/modulated_{timestamp}.wav'
    base_freq = float(base_freq.get())
    offset = float(offset.get())

    if not audio:
        messagebox.showerror("Error", "Please select an input file")
        return

    progress.set(0)
    # Run the transmitter function
    binary_data, modulated_signal, sampling_rate = run(audio, output, base_freq, offset)
    progress.set(100)
    # Plot the original and modulated waveforms
    plot(audio, orig_plot, "Original Audio Waveform", binary_data, sampling_rate, modulated=False)
    plot(modulated_signal, fsk_plot, "Modulated Signal Waveform", binary_data, sampling_rate, modulated=True)
    messagebox.showinfo("Success", f"Modulated audio saved to {output}")

def plot(signal, canvas, title, binary_data=None, sampling_rate=None, modulated=False):
    # Plot the waveform of the given signal
    if isinstance(signal, str):
        signal, samplerate = sf.read(signal)
    
    fig = Figure(figsize=(8, 4))
    ax = fig.add_subplot(111)
    
    sample = 1000  # Number of samples to plot

    if binary_data is not None and sampling_rate is not None:
        # Plot binary data section
        present = np.where(binary_data == 1)[0]
        if len(present) > 0:
            start = present[0]
            end = start + sample if len(present) > sample else present[-1]
            signal_sample = signal[start:end]
            ax.plot(signal_sample)
            ax.set_xlim(0, len(signal_sample))
            ax.set_title(f"{title}")
        else:
            ax.plot(signal)
            ax.set_title(title)
    else:
        # Plot signal without binary data
        ax.plot(signal[:sample])
        ax.set_title(title)
    
    ax.set_xlabel("Sample Index")
    ax.set_ylabel("Amplitude")

    canvas.figure = fig
    canvas.draw()

def display(run):
    # Launch the GUI for FSK modulation transmitter
    root = tk.Tk()
    root.title("FSK Modulation Transmitter")

    in_file = tk.StringVar()
    base_freq = tk.StringVar(value="1500")
    offset = tk.StringVar(value="1000")
    progress = tk.IntVar()

    tk.Label(root, text="Input Audio File:").grid(row=0, column=0, padx=10, pady=5)
    tk.Entry(root, textvariable=in_file, width=50).grid(row=0, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=lambda: browse(in_file)).grid(row=0, column=2, padx=10, pady=5)

    tk.Label(root, text="Base Frequency (Hz):").grid(row=1, column=0, padx=10, pady=5)
    tk.Entry(root, textvariable=base_freq, width=20).grid(row=1, column=1, padx=10, pady=5, sticky="w")

    tk.Label(root, text="Frequency Offset (Hz):").grid(row=2, column=0, padx=10, pady=5)
    tk.Entry(root, textvariable=offset, width=20).grid(row=2, column=1, padx=10, pady=5, sticky="w")

    loading = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", variable=progress)
    loading.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

    tk.Button(root, text="Modulate", command=lambda: start(in_file, base_freq, offset, run, progress, orig_plot, fsk_plot)).grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    # Add canvas for plotting original waveform
    fig, ax = plt.subplots(figsize=(8, 4))
    orig_plot = FigureCanvasTkAgg(fig, master=root)
    orig_plot.get_tk_widget().grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    # Add canvas for plotting modulated waveform
    fig, ax = plt.subplots(figsize=(8, 4))
    fsk_plot = FigureCanvasTkAgg(fig, master=root)
    fsk_plot.get_tk_widget().grid(row=6, column=0, columnspan=3, padx=10, pady=10)

    root.mainloop()
