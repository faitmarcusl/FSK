import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.signal import welch
from matplotlib.figure import Figure
import time

def browse(in_file):
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
    if file_path:
        in_file.set(file_path)

def start(in_file, base_freq, offset, run, progress, modulated_freq_plot, demodulated_freq_plot):
    audio = in_file.get()
    timestamp = int(time.time())
    output = f'C:/Users/Jerwin_JIL/Downloads/FSK-F/demodulated/demodulated_{timestamp}.wav'
    base_freq = float(base_freq.get())
    offset = float(offset.get())

    if not audio:
        messagebox.showerror("Error", "Please select an input file")
        return

    progress.set(0)
    fsk_signal, sampling_rate, instantaneous_frequency = run(audio, output, base_freq, offset)
    progress.set(100)
    plot_frequency_domain(fsk_signal, modulated_freq_plot, "Modulated Signal Frequency Spectrum", sampling_rate)
    plot_frequency_domain(instantaneous_frequency, demodulated_freq_plot, "Demodulated Signal Frequency Spectrum", sampling_rate)
    messagebox.showinfo("Success", f"Demodulated audio saved to {output}")

def plot_frequency_domain(signal, canvas, title, sampling_rate):
    fig = Figure(figsize=(6, 3))  # Adjusted figure size here
    ax = fig.add_subplot(111)
    f, Pxx = welch(signal, fs=sampling_rate, nperseg=1024)
    ax.semilogy(f, Pxx)
    ax.set_title(title)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Power/Frequency (dB/Hz)")
    canvas.figure = fig
    canvas.draw()

def display(run):
    root = tk.Tk()
    root.title("FSK Demodulation Receiver")

    in_file = tk.StringVar()
    base_freq = tk.StringVar(value="1500")
    offset = tk.StringVar(value="1000")
    progress = tk.IntVar()

    tk.Label(root, text="Input Modulated File:").grid(row=0, column=0, padx=10, pady=5)
    tk.Entry(root, textvariable=in_file, width=50).grid(row=0, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=lambda: browse(in_file)).grid(row=0, column=2, padx=10, pady=5)

    tk.Label(root, text="Base Frequency (Hz):").grid(row=1, column=0, padx=10, pady=5)
    tk.Entry(root, textvariable=base_freq, width=20).grid(row=1, column=1, padx=10, pady=5, sticky="w")

    tk.Label(root, text="Frequency Offset (Hz):").grid(row=2, column=0, padx=10, pady=5)
    tk.Entry(root, textvariable=offset, width=20).grid(row=2, column=1, padx=10, pady=5, sticky="w")

    loading = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", variable=progress)
    loading.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

    tk.Button(root, text="Demodulate", command=lambda: start(in_file, base_freq, offset, run, progress, modulated_freq_plot, demodulated_freq_plot)).grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    fig_modulated = Figure(figsize=(6, 3))  # Adjusted figure size here
    modulated_freq_plot = FigureCanvasTkAgg(fig_modulated, master=root)
    modulated_freq_plot.get_tk_widget().grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    fig_demodulated = Figure(figsize=(6, 3))  # Adjusted figure size here
    demodulated_freq_plot = FigureCanvasTkAgg(fig_demodulated, master=root)
    demodulated_freq_plot.get_tk_widget().grid(row=6, column=0, columnspan=3, padx=10, pady=10)

    root.mainloop()
