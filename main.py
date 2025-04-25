import subprocess
import tkinter as tk
from tkinter import messagebox

class KeyloggerControlPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger & Detection Control Panel")
        self.root.geometry("400x300")

        tk.Label(root, text="Select an Option", font=("Arial", 14, "bold")).pack(pady=10)

        self.running_process = None

        self.start_keylogger_btn = tk.Button(root, text="Run Keylogger", font=("Arial", 12), bg="red", fg="white", command=self.run_keylogger)
        self.start_keylogger_btn.pack(pady=5)

        self.start_detector_btn = tk.Button(root, text="Run Keylogger Detector", font=("Arial", 12), bg="green", fg="white", command=self.run_detector)
        self.start_detector_btn.pack(pady=5)

        self.stop_btn = tk.Button(root, text="Stop Program", font=("Arial", 12), bg="gray", fg="white", command=self.stop_program, state=tk.DISABLED)
        self.stop_btn.pack(pady=10)

        self.exit_btn = tk.Button(root, text="Exit", font=("Arial", 12, "bold"), bg="black", fg="white", command=root.quit)
        self.exit_btn.pack(pady=10)

    def run_keylogger(self):
        """Runs keylogger_gui.py with GUI and logging."""
        if self.running_process:
            messagebox.showwarning("Warning", "A program is already running. Stop it before launching another.")
            return
        self.running_process = subprocess.Popen(["python", "keylogger_gui.py"])
        self.stop_btn.config(state=tk.NORMAL)
        messagebox.showinfo("Keylogger", "Keylogger GUI is running and logging to logs.txt!")

    def run_detector(self):
        if self.running_process:
            messagebox.showwarning("Warning", "A program is already running. Stop it before launching another.")
            return
        self.running_process = subprocess.Popen(["python", "keylogger_detector_gui.py"])
        self.stop_btn.config(state=tk.NORMAL)
        messagebox.showinfo("Keylogger Detector", "Keylogger Detector is running!")

    def stop_program(self):
        if self.running_process:
            self.running_process.terminate()
            self.running_process = None
            self.stop_btn.config(state=tk.DISABLED)
            messagebox.showinfo("Stopped", "The running program has been stopped.")
        else:
            messagebox.showwarning("Warning", "No program is currently running.")

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerControlPanel(root)
    root.mainloop()
