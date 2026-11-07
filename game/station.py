from dataclasses import dataclass, field
LISTEN_VOLUME=0.25

@dataclass
class Station:
    frequency: float
    audio_file: str=""
    required_listen_time: float=0.0
    radius: float=0.6
    journal_text: str=""
    next_frequencies: list[float]=field(default_factory=list)
    requirements: list[str]=field(default_factory=list)
    discovered: bool =False
    listen_progress: float=0.0
    heard_fully: bool=False
    transcribed: bool=False

    @property
    def loggable(self):
        return bool(self.journal_text.strip())
    def volume_at(self, freq):
        distance= abs(freq - self.frequency)
        if distance >= self.radius:
            return 0.0
        return 1.0 -(distance / self.radius)
