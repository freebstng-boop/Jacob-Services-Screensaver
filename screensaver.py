import tkinter as tk
from time import strftime
from PIL import Image, ImageTk, ImageDraw
0 * * * * export DISPLAY=:0 && /usr/bin/python3 /home/pi/Jacob-Services-Screensaver/updater.py
os.environ['DISPLAY'] = ':0'


class Screensaver:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.configure(background='black')
        
        # 1. Load Background Image
        # Replace 'background.jpg' with your actual image path
        self.bg_image = Image.open("background.jpg")
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.bg_image = self.bg_image.resize((self.screen_width, self.screen_height), Image.LANCZOS)
        
        # 2. Create the Dark Overlay (Bottom Gradient)
        overlay = Image.new('RGBA', (self.screen_width, self.screen_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        # Draw a semi-transparent black rectangle at the bottom
        overlay_height = int(self.screen_height * 0.3)
        draw.rectangle([0, self.screen_height - overlay_height, self.screen_width, self.screen_height], 
                       fill=(0, 0, 0, 160)) # 160 is the alpha/transparency
        
        self.bg_image.paste(overlay, (0, 0), overlay)
        self.final_bg = ImageTk.PhotoImage(self.bg_image)
        
        # 3. Canvas Setup
        self.canvas = tk.Canvas(self.root, width=self.screen_width, height=self.screen_height, 
                               highlightthickness=0, bd=0)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.final_bg, anchor="nw")

        # 4. UI Elements
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

        # 5. Interaction to Close
        self.root.bind("<Any-KeyPress>", lambda e: self.root.destroy())
        self.root.bind("<Button-1>", lambda e: self.root.destroy())
        
        self.update_clock()
        self.root.mainloop()

    def update_clock(self):
        current_time = strftime('%H:%M')
        current_date = strftime('%A, %B %d')
        self.canvas.itemconfig(self.time_label, text=current_time)
        self.canvas.itemconfig(self.date_label, text=current_date)
        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    Screensaver()
