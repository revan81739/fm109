import pygame
import os
from game.stations import STATIONS

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.set_num_channels(16)
        self.static=pygame.mixer.Sound("sounds/static.wav")
        self.static.set_volume(0.25)
        self.station_channels=[]
        self.load_stations()
    def start_static(self):
        self.static.play(loops=-1)
    def stop_static(self):
        self.static.stop()


    def load_stations(self):
        for station in STATIONS:
            self.add_station(station)

    def add_station(self, station):
        if not os.path.exists(station.audio_file):
            print(f"[audio] missing {station.audio_file}, using placeholder timing")
            if station.required_listen_time <=0:
                station.required_listen_time=8.0
            return
        sound =pygame.mixer.Sound(station.audio_file)
        if station.required_listen_time<=0:
            station.required_listen_time=sound.get_length()

        channel =pygame.mixer.find_channel()
        if channel is None:
            raise RuntimeError("No free audio channels")
        channel.play(sound, loops=-1)
        channel.set_volume(0)
        self.station_channels.append((station, channel))
       
    def update_stations(self, frequency):
        for station, channel in self.station_channels:
            channel.set_volume(station.volume_at(frequency))