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
        self.root.bind("<MouseWheel>", self.turn_knob)

    def build_ui(self):
        main=tk.Frame(self.root, bg=theme.BACKGROUND)
        main.pack(fill="both", expand=True)

        self.canvas= tk.Canvas(
            main,
            width=900,
            height=620,
            bg=theme.BACKGROUND,
            highlightthickness=0
        )
        self.canvas.pack()

        image =Image.open("assets/radio2.png")
        image=image.resize((700, 450), Image.Resampling.NEAREST)

        self.radio_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(
            450,
            240,
            image=self.radio_image
        )

        self.frequency_text =self.canvas.create_text(
            310,
            220,
            text="95.0",
            fill="#8CFFB5",
            font=("Consolas", 26, "bold")
        )


    def turn_knob(self, event):
        freq=self.frequency.get()
        if event.delta > 0:
            freq +=0.1
        else:
            freq -= 0.1
        freq =max(88.0, min(108.0, freq))
        self.frequency.set(freq)
        self.update_frequency(freq)
    
    
    def update_frequency(self, value):
        freq = float(value)
        self.canvas.itemconfig(
            self.frequency_text,
            text=f"{freq:.1f}"
        )
        

        