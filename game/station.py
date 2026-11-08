from dataclasses import dataclass, field
STATION_WIDTH=1.6

@dataclass
class Station:
    name= str
    frequency: float
    audio_files: list[str]
    journal_text: str=""
    width: float= STATION_WIDTH
    requirements: list[str]=field(default_factory=list)
    total_lenth: float=0.0
    heard_fully: bool=False
    transcribed: bool=False

    @property
    def end(self):
        return self.frequency + self.width

    @property
    def loggable(self):
        return bool(self.journal_text.strip())
    def contains(self, freq):
        return self.frequency - 1e-9 <= freq <= self.end + 1e-9