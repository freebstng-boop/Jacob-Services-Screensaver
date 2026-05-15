import tkinter as tk
import os
from time import strftime
from PIL import Image, ImageTk, ImageDraw

# 1. Fixed Display for your Pi 3A+
os.environ['DISPLAY'] = ':1'

class Screensaver:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.configure(background='black')
        
        # Ensure we are in the correct directory to find background.jpg
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # 2. Load Background Image
        try:
            self.bg_image = Image.open("background.jpg")
        except FileNotFoundError:
            # Create a plain black image if background.jpg is missing
            self.bg_image = Image.new('RGB', (800, 480), color='black')
            print("Warning: background.jpg not found, using black background.")

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.bg_image = self.bg_image.resize((self.screen_width, self.screen_height), Image.LANCZOS)
        
        # 3. Create the Dark Overlay (Bottom Gradient)
        overlay = Image.new('RGBA', (self.screen_width, self.screen_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        overlay_height = int(self.screen_height * 0.3)
        draw.rectangle([0, self.screen_height - overlay_height, self.screen_width, self.screen_height], 
                       fill=(0, 0, 0, 160)) 
        
        self.bg_image.paste(overlay, (0, 0), overlay)
        self.final_bg = ImageTk.PhotoImage(self.bg_image)
        
        # 4. Canvas Setup
        self.canvas = tk.Canvas(self.root, width=self.screen_width, height=self.screen_height, 
                                highlightthickness=0, bd=0)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.final_bg, anchor="nw")

        # 5. UI Elements
        # Greeting (Top Left)
        self.canvas.create_text(50, 50, text="Good Morning, Bradley", fill="white", 
                                font=("Helvetica", 24), anchor="nw")

        # Big Clock (Bottom Left)
        self.time_label = self.canvas.create_text(50, self.screen_height - 180, text="", 
                                                 fill="white", font=("Helvetica Bold", 120), anchor="sw")
        
        # Date (Below Clock)
        self.date_label = self.canvas.create_text(50, self.screen_height - 130, text="", 
                                                 fill="white", font=("Helvetica", 32), anchor="sw")

        # Weather/Location (Bottom Right)
        weather_text = "72°F Partly Cloudy\nQueen Creek, AZ"
        self.canvas.create_text(self.screen_width - 50, self.screen_height - 100, text=weather_text, 
                                fill="white", font=("Helvetica", 28), anchor="se", justify="right")

        # 6. Interaction to Close
        self.root.bind("<Any-KeyPress>", lambda e: self.root.destroy())
        self.root.bind("<Button-1>", lambda e: self.root.destroy())
        
        self.update_clock()
        self.root.mainloop()

    def update_clock(self):
        # Use %I for 12-hour clock or %H for 24-hour
        current_time = strftime('%I:%M %p') 
        current_date = strftime('%A, %B %d')
        self.canvas.itemconfig(self.time_label, text=current_time)
        self.canvas.itemconfig(self.date_label, text=current_date)
        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    Screensaver()
