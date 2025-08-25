from dataclasses import dataclass
@dataclass
class Event:
    coordinates : [float, float, float]
    t0: float