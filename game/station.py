from dataclasses import dataclass, field

@dataclass
class Station:
    frequency: float
    audio_file: str
    required_listen_time: float
    journal_text: str
    next_frequencies: list[float]=field(default_factory=list)
    requirements: list[str]=field(default_factory=list)
    discovered: bool =False
