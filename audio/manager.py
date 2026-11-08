import pygame
import os
import time
from game.stations import STATIONS, get_station
STATIC_IDLE=0.25
STATIC_ON_STATION=0.3

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.set_num_channels(8)
        pygame.mixer.set_reserved(2)

        self.static=pygame.mixer.Sound("sounds/static.wav")
        self.static_channel=pygame.mixer.Channel(0)
        self.station_channel=pygame.mixer.Channel(1)
        self.sounds={}
        self.active_station=None
        self.active_started=0.0
        self.load_stations()


    def start_static(self):
        self.static_channel.play(self.static, loops=-1)
        self.static_channel.set_volume(STATIC_IDLE)
    def stop_static(self):
        self.static_channel.stop()


    def load_stations(self):
        for station in STATIONS:
            loaded=[]
            for path in station.audio_files:
                if os.path.exists(path):
                    loaded.append(pygame.mixer.Sound(path))
                else:
                    print(f"[audio] missing {path}")
                self.sounds[station.name]=loaded
                station.total_length=(
                    sum(s.get_length() for s in loaded) if loaded else 8.0
                )


    def tune(self, frequency):
        station=get_station(frequency)
        if station is self.active_station:
            return station
        self.station_channel.stop()
        self.active_station=station

        if station is None:
            self.static_channel.set_volume(STATIC_IDLE)
            return None
        sounds=self.sounds[station.name]

        if sounds:
            self.station_channel.play(sounds[0])
            for extra in sounds[1:]:
                self.station_channel.queue(extra)
        self.active_started=time.monotonic()
        self.static_channel.set_volume(STATIC_ON_STATION)
        return station
    def elapsed(self):
        if self.active_station is None:
            return 0.0
        return time.monotonic() - self.active_started
    