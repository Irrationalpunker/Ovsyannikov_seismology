from dataclasses import dataclass
@dataclass
class Station:
    id: int
    coordinates : [float, float, float]