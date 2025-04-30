import psutil
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Suspicious keylogger indicators
suspicious_filenames = ["logs.txt", "keylogger.py", "keyloggerf.py"]
suspicious_processes = ["pynput", "hook", "logger", "keylogger"]

class KeyloggerDetectorAndKillerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger Detector, Killer & Remover")
        self.root.geometry("650x500")

        self.label = tk.Label(root, text="Keylogger Detection System", font=("Arial", 16, "bold"))
        self.label.pack(pady=10)

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 12))
        self.text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.text_area.config(state=tk.DISABLED)
        self.text_area.insert(tk.END, "Click 'Scan' to detect running keyloggers and files...\n")

        self.scan_button = tk.Button(root, text="Scan & Kill Keyloggers", font=("Arial", 12, "bold"), bg="blue", fg="white", command=self.scan_for_keyloggers)
        self.scan_button.pack(pady=5)

        self.exit_button = tk.Button(root, text="Exit", font=("Arial", 12, "bold"), bg="black", fg="white", command=self.exit_program)
        self.exit_button.pack(pady=5)

    def log_message(self, message):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.config(state=tk.DISABLED)
        self.text_area.yview(tk.END)

    def clear_log(self):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete("1.0", tk.END)
        self.text_area.config(state=tk.DISABLED)

    def detect_suspicious_files(self):
        suspicious_found = []
        for foldername, subfolders, filenames in os.walk("."):
            for filename in filenames:
                if filename.lower() in suspicious_filenames:
                    full_path = os.path.join(foldername, filename)
                    suspicious_found.append(full_path)
        return suspicious_found

    def detect_suspicious_processes(self):
        found_processes = []
        for process in psutil.process_iter(['pid', 'name']):
            try:
                if any(suspicious in process.info['name'].lower() for suspicious in suspicious_processes):
                    found_processes.append((process.info['name'], process.info['pid']))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return found_processes

    def scan_for_keyloggers(self):
        self.clear_log()
        self.log_message("🔍 Scanning for keylogger files and running processes...")

        detected_files = self.detect_suspicious_files()
        found_processes = self.detect_suspicious_processes()

        if not detected_files and not found_processes:
            self.log_message("✅ No keyloggers detected.")
            return

        if detected_files:
            self.log_message("\n🗂️ Suspicious Files Found:")
            for file in detected_files:
                self.log_message(f" - {file}")

        if found_processes:
            self.log_message("\n🛑 Suspicious Processes Running:")
            for name, pid in found_processes:
                self.log_message(f" - {name} (PID: {pid})")

        # Ask user before taking action
        confirm = messagebox.askyesno("Confirm Removal", "⚠️ Suspicious items found.\nDo you want to delete files and kill processes?")
        if confirm:
            self.remove_keyloggers(detected_files, found_processes)

    def remove_keyloggers(self, files, processes):
        self.log_message("\n🚨 Attempting to remove detected keyloggers...")

        # Delete suspicious files
        for file_path in files:
            try:
                os.remove(file_path)
                self.log_message(f"✅ Deleted file: {file_path}")
            except Exception as e:
                self.log_message(f"❌ Failed to delete file {file_path}: {e}")

        # Kill suspicious processes
        for name, pid in processes:
            try:
                psutil.Process(pid).terminate()
                self.log_message(f"✅ Terminated process: {name} (PID: {pid})")
            except Exception as e:
                self.log_message(f"❌ Failed to terminate process {name} (PID: {pid}): {e}")

        messagebox.showinfo("Threats Removed", "🛡️ All detected threats have been handled!")

    def exit_program(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerDetectorAndKillerGUI(root)
    root.mainloop()