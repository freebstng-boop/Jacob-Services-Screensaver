import requests
import subprocess
import tkinter as tk
from tkinter import messagebox
import os
import time

# 1. Force the display to the main monitor
os.environ['DISPLAY'] = ':0'

# 2. Ensure we are in the correct directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- CONFIGURATION ---
# IMPORTANT: This must be the RAW link. 
# Go to GitHub, click version.txt, click 'Raw', and copy that URL.
VERSION_URL = "https://raw.githubusercontent.com/freebstng-boop/Jacob-Services-Screensaver/main/version.txt"
LOCAL_VERSION_FILE = "version.txt"

def check_for_updates():
    try:
        # Give the network a second to breathe if running at boot
        time.sleep(2) 

        # 1. Get the latest version number from GitHub
        response = requests.get(VERSION_URL, timeout=10)
        response.raise_for_status() # Check if the URL actually exists
        
        remote_version = response.text.strip()

        # 2. Read local version
        if os.path.exists(LOCAL_VERSION_FILE):
            with open(LOCAL_VERSION_FILE, "r") as f:
                local_version = f.read().strip()
        else:
            local_version = "0.0"

        # 3. Compare (Print for debugging if you run manually)
        print(f"Local: '{local_version}' | Remote: '{remote_version}'")
        
        if remote_version != local_version:
            print("Update detected!")
            prompt_update(remote_version)
        else:
            print("No update needed.")
            
    except Exception as e:
        print(f"Update check failed: {e}")

def prompt_update(new_version):
    root = tk.Tk()
    root.withdraw() 
    
    # Ensure it sits on top of everything
    root.attributes("-topmost", True)
    
    title_text = "Software Update"
    message_text = f"A new version ({new_version}) is available.\n\nWould you like to install it now?"
    
    # This makes the popup grab focus
    root.focus_force()
    
    answer = messagebox.askyesno(title_text, message_text)
    
    if answer:
        perform_update()
    
    root.destroy()

def perform_update():
    try:
        # Use Git to pull the new code
        subprocess.run(["git", "pull"], check=True)
        print("Update successful!")
        
        # Optional: Restart the Pi or the screensaver
        # subprocess.run(["pkill", "-f", "screensaver.py"])
        
    except subprocess.CalledProcessError:
        print("Git pull failed. Make sure you haven't edited files locally on the Pi.")

if __name__ == "__main__":
    check_for_updates()
