import tkinter as tk
from PIL import Image, ImageTk
from tkinter import scrolledtext
from ui import theme
import math
import time
from audio.manager import AudioManager
from game.stations import STATIONS, get_station

INTRO_TEXT="""\
You were sent up the Windwhisper Ridge storm lookout to watch the tree line before the season turned\
The road line was submerged behind you this afternoon

The generator is dead. The phone line is silent\
All you have is this old radio

Since the air pressure changed, it's been picking up things it shouldnt be\
Weather broadcasts from 30 years ago. Songs from another era. Conversations, bleeding into the signal

Someone is trying to tell you something

Listen carefully. If a transmission feels important, log it before its gone"""

class RadioWindow:
    def __init__(self, root):
        self.root=root
        self.root.title("FM 109")
        self.root.geometry("1000x700")
        self.root.configure(bg=theme.BACKGROUND)
        self.frequency = tk.DoubleVar(value=95.0)
        self.audio =AudioManager()
        
        self.scale_factor =4
        self.radio_center_x=500
        self.radio_center_y=330
        self.knob_frame_count = 23
        self.min_frequency=88.0
        self.max_frequency= 108.0
        self.knob_center_x=624
        self.knob_center_y=278
        self.knob_visualoffset_x=-124
        self.knob_visualoffset_y=54
        self.dragging = False
        self.last_mouse_angle=None
        self.drag_frequency= 95.0
        self.log_button_x=430
        self.log_button_y=365
        self.current_station =None
        self.last_check_time=time.monotonic()
        self.build_ui()

        self.show_intro()

    def build_ui(self):
        main=tk.Frame(self.root, bg=theme.BACKGROUND)
        main.pack(fill="both", expand=True)

        self.canvas= tk.Canvas(
            main,
            bg=theme.BACKGROUND,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag_knob)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)
        self.draw_radio()
        self.draw_screen()
        self.draw_knob()
        self.draw_log_button()
        journal_frame =tk.LabelFrame(
            main,
            text=" Storm lookout logs",
            bg=theme.BACKGROUND,
            fg="green",
            font=("Consolas", 12, "bold")
        )
        journal_frame.pack(fill="both", expand=False, padx=20, pady=5)
        self.journal_area= scrolledtext.ScrolledText(
            journal_frame,
            bg="#111111",
            fg="#90F090",
            insertbackground="green",
            font=("Consolas", 11),
            height=6,
            state="disabled"
        )
        self.journal_area.pack(fill="both", expand=True, padx=5, pady=5)
        
    def draw_radio(self):
        image=Image.open("assets/radio2.png")
        
        width=image.width * self.scale_factor
        height=image.height*self.scale_factor
        
        image =image.resize((width, height), Image.Resampling.NEAREST)
        self.radio_image =ImageTk.PhotoImage(image)

        self.radio= self.canvas.create_image(
            self.radio_center_x,
            self.radio_center_y,
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
        sheet =Image.open("assets/knobsheet2.png").convert("RGBA")
        base_frame_width=128
        self.knob_frame_count=sheet.width // base_frame_width
        frame_width=base_frame_width
        frame_height =sheet.height
        if sheet.width % self.knob_frame_count !=0:
            raise ValueError("Spreite sheet width must divide into frame count smh")
    
        self.knob_frames =[]
        for i in range(self.knob_frame_count):
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

        visual_x=self.knob_center_x + self.knob_visualoffset_x
        visual_y=self.knob_center_y +self.knob_visualoffset_y
        self.knob= self.canvas.create_image(
            visual_x,
            visual_y,
            image=self.knob_frames[0]
         )
        self.update_knob()

    def show_intro(self):
        win=tk.TopLevel(self.root)
        self.intro_win=win
        win.title("Windwhisper Ridge Lookout")
        win.configure(bg=theme.PANEL)
        win.resizable(False, False)
        win.transient(self.root)
        width, height=560, 440

        self.root.update_idletasks()
        x= self.root.winfo_x() + (self.root.winfo_width() - width) // 2
        y=   self.root.winfo_y() +(self.root.winfo_height() -height) //2
        win.geometry(f"{width}x{height}+{x}+{y}")

        tk.Label(
            win,
            text="WINDWHISPER RIDGE LOOKOUT",
            bg=theme.PANEL,
            fg=theme.GREEN,
            font=theme.TITLE
        ).pack(pady=(18, 8))
        text= tk.Text(
            win,
            wrap="word",
            bg=theme.PANEL,
            fg=theme.TEXT,
            font=("Consolas", 12),
            relief="flat",
            padx=20,
            pady=5,
            highlightthickness=0,
            cursor="arrow"
        )
        text.insert("1.0", INTRO_TEXT)
        text.config(state="disabled")
        text.pack(fill="both", expand=True, padx=10)

        tk.Button(
            win,
            text="Switch on the radio",
            command=self.close_intro,
            bg=theme.BUTTON,
            fg=theme.GREEN,
            activebackground=theme.BUTTON_HOVER,
            activeforeground=theme.GREEN,
            font=("Consolas", 12, "bold"),
            relief="flat",
            padx=14,
            pady=6
        ).pack(pady=14)
        win.protocol("WM_DELETE_WINDOW", self.close_intro)
        win.grab_set()
        win.focus_Set()
    
    def close_intro(self):
        self.intro_win.grab_release()
        self.intro_win.destroy()
        self.audio.start_static()
        self.audio.update_stations(self.frequency.get())
        self.last_check_time= time.monotonic()
        self.check_station_timer()
        
    def start_drag(self, event):
        mouse_x= self.canvas.canvasx(event.x)
        mouse_y =self.canvas.canvasy(event.y)
        dx =mouse_x -self.knob_center_x
        dy=mouse_y-self.knob_center_y
        distance= math.sqrt(dx**2+ dy**2)

        if distance>75:
            return
        self.dragging= True
        self.last_mouse_angle =math.degrees(
            math.atan2(dy, dx)
        )
        self.drag_frequency=self.frequency.get()

    def drag_knob(self, event):
        if not self.dragging:
            return
        mouse_x= self.canvas.canvasx(event.x)
        mouse_y=self.canvas.canvasy(event.y)

        dx= mouse_x - self.knob_center_x
        dy = mouse_y -self.knob_center_y
        current_angle=math.degrees(
            math.atan2(dy, dx)
        )

        angle_difference =(current_angle - self.last_mouse_angle)
        if angle_difference > 180:
            angle_difference -= 360
        elif angle_difference< -180:
            angle_difference += 360

        self.last_mouse_angle= current_angle
        frequency_change= angle_difference / 360 * 20
        self.drag_frequency += frequency_change
        self.drag_frequency = max(
            88.0,
            min(108.0, self.drag_frequency)
        )
        snapped_frequency=round(self.drag_frequency, 1)
        self.frequency.set(snapped_frequency)
        self.update_frequency(snapped_frequency)

    def stop_drag(self, event):
        self.dragging=False
        self.last_mouse_angle= None
    
    def update_frequency(self, value):
        freq = float(value)
        self.canvas.itemconfig(
            self.frequency_text,
            text=f"{freq:.1f}"
        )
        self.audio.update_stations(freq)
        self.update_knob()

    def update_knob(self):
        freq =self.frequency.get()
        progress=(
            (freq-self.min_frequency)
            / (self.max_frequency - self.min_frequency)
        )
        frame_index =round(progress*(self.knob_frame_count-1))
        frame_index=max(0, min(self.knob_frame_count-1, frame_index))


        self.canvas.itemconfig(
            self.knob,
            image=self.knob_frames[frame_index]
        )

    def check_station_timer(self):
        now= time.monotonic()
        delta_time =min(now - self.last_check_time, 0.5)
        self.last_check_time= now
        station =get_station(round(self.frequency.get(), 1))
        self.current_station= station
        if (station and station.loggable
            and not station.transcribed
            and not station.heard_fully):
            station.listen_progress += delta_time
            if station.listen_progress >= station.required_listen_Time:
                station.heard_fully =True

        can_log= bool(
            station and station.loggable
            and station.heard_fully and not station.transcribed
        )
        self.canavs.itemconfigure(
            self.log_button_window,
            state="normal" if can_log else "hidden"
        )

    def transcribe_current(self):
        station =self.current_station
        if not station or not station.heard_fully or station.transcribed:
            return
        station.transcribed=True
        self.add_journal_entry(station.frequency, station.journal_text)
        self.canvas.itemconfigure(self.log_button_window, state="hidden")

    def add_journal_entry(self, freq, text):
        self.journal_area.config(state="normal")
        entry=f"[{freq:.1f} Mhz] Transcribed Audio:\n{text.strip()}\n\n"
        self.journal_area.insert(tk.END, entry)
        self.journal_area.see(tk.END)
        self.journal_area.config(state="disabled")