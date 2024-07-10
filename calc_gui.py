import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt

class BER_SNR_GUI:
    def __init__(self, master, calculate_metrics):
        self.master = master
        self.calculate_metrics = calculate_metrics
        self.master.title("BER and SNR Calculator")

        self.calculate_button = tk.Button(master, text="Calculate BER and SNR", command=self.on_calculate_metrics)
        self.calculate_button.pack(pady=20)

        self.plot_button = tk.Button(master, text="Plot BER vs SNR", command=self.plot_ber_vs_snr)
        self.plot_button.pack(pady=20)

        self.ber_snr_data = []

    def select_files(self, title):
        return filedialog.askopenfilenames(title=title, filetypes=[("Audio files", "*.wav")])

    def on_calculate_metrics(self):
        original_file = filedialog.askopenfilename(title="Select Original Audio File", filetypes=[("Audio files", "*.wav")])
        demodulated_files = self.select_files("Select Demodulated Audio Files")

        if not original_file or not demodulated_files:
            messagebox.showerror("File Error", "Original file and at least one demodulated file need to be selected.")
            return

        try:
            for demodulated_file in demodulated_files:
                ber, snr = self.calculate_metrics(original_file, demodulated_file)
                self.ber_snr_data.append((ber, snr))
                messagebox.showinfo("Results", f"File: {demodulated_file}\nBit Error Rate (BER): {ber:.6f}\nSignal-to-Noise Ratio (SNR): {snr:.2f} dB")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def plot_ber_vs_snr(self):
        if not self.ber_snr_data:
            messagebox.showerror("Plot Error", "No data to plot.")
            return

        bers, snrs = zip(*self.ber_snr_data)
        plt.figure()
        plt.plot(snrs, bers, marker='o')
        plt.xlabel('SNR (dB)')
        plt.ylabel('BER')
        plt.title('BER vs SNR')
        plt.grid(True)
        plt.show()