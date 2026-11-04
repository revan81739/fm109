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
        self.scale_factor =4
        self.build_ui()
    
        self.root.bind("<MouseWheel>", self.turn_knob)

    def build_ui(self):
        main=tk.Frame(self.root, bg=theme.BACKGROUND)
        main.pack(fill="both", expand=True)

        self.canvas= tk.Canvas(
            main,
            bg=theme.BACKGROUND,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.draw_radio()
        self.draw_screen()
        self.draw_knob()
        

    def draw_radio(self):
        image=Image.open("assets/radio2.png")
        
        width=image.width * self.scale_factor
        height=image.height*self.scale_factor
        
        image =image.resize((width, height), Image.Resampling.NEAREST)
        self.radio_image =ImageTk.PhotoImage(image)

        self.radio= self.canvas.create_image(
            500,
            330,
            image=self.radio_image
        )

    def draw_screen(self):
        self.frequency_text =self.canvas.create_text(
            430,
            315,
            text="95.0",
            fill="#90F090",
            font=("Consolas",24,"bold")
        )

    def draw_knob(self):
        sheet =Image.open("assets/knob_sheet.png").convert("RGBA")
        frame_width=sheet.width // 14
        frame_height =sheet.height
        self.knob_frames =[]
        
        for i in range(14):
            left=i*frame_width
            top=0
            right = left+frame_width
            bottom=frame_height

            frame=sheet.crop((left, top, right, bottom))

            frame= frame.resize(
                (
                    frame_width*self.scale_factor,
                    frame_height*self.scale_factor
                ),
                Image.Resampling.NEAREST
            )
            photo=ImageTk.PhotoImage(frame)
            self.knob_frames.append(photo)
        self.knob= self.canvas.create_image(
            624,
            278,
            image=self.knob_frames[0]
         )
        self.update_knob()

        
    def turn_knob(self, event):
        freq=self.frequency.get()
        if event.delta > 0:
            freq +=0.1
        else:
            freq -= 0.1
        freq =max(88.0, min(108.0, freq))
        freq=round(freq, 1)
        self.frequency.set(freq)
        self.update_frequency(freq)
    
    
    def update_frequency(self, value):
        freq = float(value)
        self.canvas.itemconfig(
            self.frequency_text,
            text=f"{freq:.1f}"
        )
        self.update_knob()

    def update_knob(self):
        freq =self.frequency.get()
        frame_index= round(
            (freq - 88.0) / 20.0 * 13
        )
        frame_index =max(0, min(13, frame_index))

        self.canvas.itemconfig(
            self.knob,
            image=self.knob_frames[frame_index]
        )
        

        