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
VERSION_URL = "https://raw.githubusercontent.com/freebstng-boop/Jacob-Services-Screensaver/main/version.txt"
LOCAL_VERSION_FILE = "version.txt"

def check_for_updates():
    try:
        time.sleep(2) 
        response = requests.get(VERSION_URL, timeout=10)
        response.raise_for_status()
        
        remote_version = response.text.strip()

        if os.path.exists(LOCAL_VERSION_FILE):
            with open(LOCAL_VERSION_FILE, "r") as f:
                local_version = f.read().strip()
        else:
            local_version = "0.0"

        print(f"Local: '{local_version}' | Remote: '{remote_version}'")
        
        if remote_version != local_version:
            prompt_update(remote_version)
            
    except Exception as e:
        print(f"Update check failed: {e}")

def prompt_update(new_version):
    root = tk.Tk()
    root.withdraw() 
    root.attributes("-topmost", True)
    
    title_text = "Software Update"
    message_text = f"A new version ({new_version}) is available.\n\nWould you like to install it now?"
    
    root.focus_force()
    answer = messagebox.askyesno(title_text, message_text)
    
    if answer:
        perform_update()
    
    root.destroy()

def perform_update():
    try:
        subprocess.run(["git", "pull"], check=True)
        print("Update successful!")
    except subprocess.CalledProcessError:
        print("Git pull failed.")

if __name__ == "__main__":
    check_for_updates()
