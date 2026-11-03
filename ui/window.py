import tkinter as tk
from PIL import Image, ImageTk
from ui import theme

class RadioWindow:
    def __init__(self, root):
        self.root=root
        self.root.title("FM 109")
        self.root.geometry("1000x700")
        self.root.configure(bg=theme.BACKGROUND)
        self.frequency = tk.DoubleVar(value=95.0)
        self.build_ui()

    def build_ui(self):
        main=tk.Frame(self.root, bg=theme.BACKGROUND)

        main.pack(fill="both", expand=True)
        title= tk.Label(main, text = "FM 109", bg =theme.BACKGROUND, fg=theme.GREEN, font=theme.TITLE)
        title.pack(pady=15)
        image = Image.open("assets/radio1.png")
        image =image.resize((500, 320), Image.Resampling.NEAREST)
        
        self.radio_image= ImageTk.PhotoImage(image)
        
        image_label =tk.Label(
            main,
            image=self.radio_image,
            bg=theme.BACKGROUND,
        )
        
        
        
        image_label.pack()

        self.freq_label = tk.Label(
            main,
            text= "95.0 MHz",
            bg = theme.BACKGROUND,
            fg = theme.TEXT,
            font =theme.FREQUENCY
        )
        self.freq_label.pack(pady=20)

        slider = tk.Scale(
            main,
            from_=88.0,
            to=108.0,
            orient= "horizontal",
            resolution = 0.1,
            variable =self.frequency,
            command =self.update_frequency,
            length = 500,
            bg =theme.PANEL,
            fg =theme.TEXT,
            troughcolor = "#444444",
            highlightthickness =0,
        )
        slider.pack()

        self.signal = tk.Label(
            main,
            text="Signal: ----------",
            bg =theme.BACKGROUND,
            fg=theme.GREEN,
            font =theme.FONT,
        )

        self.signal.pack(pady=15)
        self.status= tk.Label(
            main,
            text="Searching...",
            bg=theme.BACKGROUND,
            fg =theme.TEXT,
            font =theme.FONT,
        )
        self.status.pack()

    def update_frequency(self, value):
        freq = float(value)
        self.freq_label.config(text=f"{freq:.1f} MHz")
        

        