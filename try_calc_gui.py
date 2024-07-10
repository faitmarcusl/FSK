import tkinter as tk
from tkinter import filedialog, messagebox
import ber_snr_processor as processor

class BER_SNR_Calculator_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BER and SNR Calculator")
        
        self.environment = tk.StringVar(value="noiseless")

        self.original_file = tk.StringVar()
        self.modulated_file = tk.StringVar()
        self.demodulated_file = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Original Audio File:").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.original_file, width=50).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Browse", command=lambda: self.browse_file(self.original_file)).grid(row=0, column=2, padx=10, pady=5)

        tk.Label(self.root, text="Modulated Audio File:").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.modulated_file, width=50).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Browse", command=lambda: self.browse_file(self.modulated_file)).grid(row=1, column=2, padx=10, pady=5)

        tk.Label(self.root, text="Demodulated Audio File:").grid(row=2, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.demodulated_file, width=50).grid(row=2, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Browse", command=lambda: self.browse_file(self.demodulated_file)).grid(row=2, column=2, padx=10, pady=5)

        tk.Label(self.root, text="Environment:").grid(row=3, column=0, padx=10, pady=5)
        tk.Radiobutton(self.root, text="Noiseless", variable=self.environment, value="noiseless").grid(row=3, column=1, sticky="w", padx=10, pady=5)
        tk.Radiobutton(self.root, text="AWGN", variable=self.environment, value="awgn").grid(row=3, column=1, padx=10, pady=5)
        tk.Radiobutton(self.root, text="Rayleigh Fading", variable=self.environment, value="rayleigh").grid(row=3, column=1, sticky="e", padx=10, pady=5)

        tk.Button(self.root, text="Calculate BER and SNR", command=self.calculate).grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    def browse_file(self, var):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
        if file_path:
            var.set(file_path)

    def calculate(self):
        original_file = self.original_file.get()
        modulated_file = self.modulated_file.get()
        demodulated_file = self.demodulated_file.get()

        if not original_file or not modulated_file or not demodulated_file:
            messagebox.showerror("Error", "Please select all files.")
            return

        environment = self.environment.get()
        ber, snr = processor.calculate_ber_snr(original_file, modulated_file, demodulated_file, environment)
        messagebox.showinfo("Results", f"Environment: {environment}\nBit Error Rate (BER): {ber}\nSignal-to-Noise Ratio (SNR): {snr} dB")

if __name__ == "__main__":
    root = tk.Tk()
    app = BER_SNR_Calculator_GUI(root)
    root.mainloop()
