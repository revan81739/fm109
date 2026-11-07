from game.station import Station, LISTEN_VOLUME
STATIONS=[
    Station(
        frequency=92.0,
        audio_file="sounds/92.wav",
        required_listen_time=4,
        journal_text="105.0-go there-write the numbers down",
        next_frequencies=[105.0]
    ),
    Station(
        frequency=105.0,
        audio_file="sounds/105.wav",
        required_listen_time=5,
        journal_text="19_6-what was that third number???",
        next_frequencies=[92.0]
    ),
    Station(
        frequency=97.0,
        audio_file="sounds/rock.wav",
        radius=0.6
    ),
]

def get_station(frequency):
    best=None
    best_volume=0.0
    for station in STATIONS:
        volume=station.volume_at(frequency)
        if volume >= LISTEN_VOLUME and volume >best_volume:
            best, best_volume =station, volume
    return best