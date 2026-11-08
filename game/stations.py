from game.station import Station
GATE_STATION="weather"
SECRET_CODE="39717"


STATIONS=[
   Station(
       name="music",
       frequency=89.0,
       audio_files=["sounds/music.wav"],
       requirements=[GATE_STATION],
   ),
   Station(
       name="weather",
       frequency=91.0,
       audio_files=["sounds/weather.wav", "sounds/entercode.wav"],
       journal_text="Enter...the...code...",
   ),
   Station(
       name="jazz",
       frequency=93.0,
       audio_files=["sounds/jazz.wav"],
       requirements=[GATE_STATION],
   ),
   Station(
       name="commercial",
       frequency=95.0,
       audio_files=["sounds/commercial.wav"],
       journal_text="Get yours for Christmas for 17 dollars",
       requirements=[GATE_STATION],
   ),
   Station(
       name="hurricane",
       frequency=97.0,
       audio_files=["sounds/hurricane.wav"],
       journal_text="A hurricane warning has been issued until 7 pm",
       requirements=[GATE_STATION],
   ),
   Station(
       name="numbers",
       frequency=99.0,
       audio_files=["sounds/numbers.wav"],
       journal_text="3...9..what is that supposed to mean?",
       requirements=[GATE_STATION],
   ),
   Station(
       name="silentnight",
       frequency=101.0,
       audio_files=["sounds/silentnight.wav"],
       requirements=[GATE_STATION],
   ),
]

def get_by_name(name):
    for station in STATIONS:
        if station.name == name:
            return station
    return None
def is_unlocked(station):
    return all(get_by_name(r).transcribed for r in station.requirements)
def get_station(frequency):
    for station in STATIONS:
        if station.contains(frequency) and is_unlocked(station):
            return station
    return None