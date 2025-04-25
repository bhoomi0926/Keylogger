import psutil
import os
import tkinter as tk
from tkinter import messagebox

# Known keylogger indicators
suspicious_files = ["logs.txt", "keylogger.py"]  # List of file names commonly associated with keyloggers
suspicious_processes = ["pynput", "hook", "logger"]  # List of keywords typically found in keylogger-related process names

def detect_keylogger_files():
    # List comprehension that checks for each suspicious file's existence
    detected_files = [file for file in suspicious_files if os.path.exists(file)]
    return detected_files
# Function to detect suspicious running processes on the system
def detect_suspicious_processes():
    found_processes = []
    for process in psutil.process_iter(['pid', 'name']):
        # Check if any suspicious keyword appears in the process name
        if any(suspicious in process.info['name'].lower() for suspicious in suspicious_processes):
            found_processes.append((process.info['name'], process.info['pid']))
    return found_processes
# Function to remove detected keyloggers (both files and processes)
def remove_keylogger():
    detected_files = detect_keylogger_files()
    found_processes = detect_suspicious_processes()

    if detected_files or found_processes:
        alert_message = "Potential Keylogger Detected!\n\n"
        
        if detected_files:
            alert_message += f"Suspicious Files Found:\n{', '.join(detected_files)}\n"
            for file in detected_files:
                try:
                    os.remove(file)
                    alert_message += f"Deleted: {file}\n"
                except Exception as e:
                    alert_message += f"Failed to delete {file}: {e}\n"

        if found_processes:
            alert_message += "Suspicious Processes Found:\n"
            for name, pid in found_processes:
                alert_message += f"{name} (PID: {pid})\n"
                try:
                    psutil.Process(pid).terminate()
                    alert_message += f"Terminated process {name} (PID: {pid})\n"
                except Exception as e:
                    alert_message += f"Failed to terminate {name}: {e}\n"

        show_alert(alert_message)
    else:
        show_alert("No keylogger detected.")

def show_alert(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning("Security Alert", message)
    root.destroy()

if __name__ == "__main__":
    remove_keylogger()
