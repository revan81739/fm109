from game.station import Station
STATIONS=[
    Station(
        frequency=92.0,
        audio_file="sounds/92.wav",
        required_listen_time=4,
        journal_text="""
105.0-go there-write the numbers down
""",
        next_frequencies=[105.0]
    ),
    Station(
        frequency=105.0,
        audio_file="sounds/105.wav",
        required_listen_time=5,
        journal_text="""
19_6-what was that third number???
""",
        next_frequencies=[92.0]
    ),

]

def get_station(frequency):
    for station in STATIONS:
        if station.fequency == frequency:
            return station
    return None