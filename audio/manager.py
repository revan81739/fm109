import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.static=pygame.mixer.Sound("sounds/static.wav")
        self.static.set_volume(0.25)

        self.stations =[]
        self.load_stations()
    def start_static(self):
        self.static.play(loops=-1)
    def stop_static(self):
        self.static.stop()


    def load_stations(self):
        self.add_station(
            sound_file="sounds/rock.wav",
            centre=97.0,
            radius=1.0
        )

    def add_station(self, sound_file, centre, radius):
        sound=pygame.mixer.Sound(sound_file)
        channel=pygame.mixer.find_channel()

        if channel is None:
            raise RuntimeError("No free audio channels")
        channel.play(sound, loops=-1)
        channel.set_volume(0)
        self.stations.append(
            {
                "centre": centre,
                "radius": radius,
                "channel": channel
            }
        )
    def update_stations(self, frequency):
        for station in self.stations:
            distance=abs(frequency - station["centre"])
            if distance>= station["radius"]:
                volume=0.0
            else:
                volume=1-(distance / station["radius"])
            station["channel"].set_volume(volume) 
    