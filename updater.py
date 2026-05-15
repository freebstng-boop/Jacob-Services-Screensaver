import requests
import subprocess
import tkinter as tk
from tkinter import messagebox
import os
os.environ['DISPLAY'] = ':0'

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Configuration
VERSION_URL = "https://github.com/freebstng-boop/Jacob-Services-Screensaver.git"
LOCAL_VERSION_FILE = "version.txt"

def check_for_updates():
    try:
        # 1. Get the latest version number from GitHub
        response = requests.get(VERSION_URL)
        remote_version = response.text.strip()

        # 2. Read local version
        if os.path.exists(LOCAL_VERSION_FILE):
            with open(LOCAL_VERSION_FILE, "r") as f:
                local_version = f.read().strip()
        else:
            local_version = "0.0"

        # 3. Compare
        if remote_version != local_version:
            prompt_update(remote_version)
            
    except Exception as e:
        print(f"Update check failed: {e}")

def prompt_update(new_version):
    root = tk.Tk()
    root.withdraw() 
    
    # This ensures the popup appears on top of the fullscreen screensaver
    root.attributes("-topmost", True)
    
    # Clean Title and Message
    title_text = "Software Update"
    message_text = f"A new version of the screensaver is available.\n\nWould you like to install it now?"
    
    # Trigger the box
    answer = messagebox.askyesno(title_text, message_text)
    
    if answer:
        perform_update()
    
    root.destroy()
    
    root.destroy()

def perform_update():
    # Use Git to pull the new code
    try:
        subprocess.run(["git", "pull"], check=True)
        # Restart the screensaver service/process here if needed
        print("Update successful!")
    except subprocess.CalledProcessError:
        print("Git pull failed.")

if __name__ == "__main__":
    check_for_updates()
