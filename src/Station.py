from dataclasses import dataclass
from geopy.location import Point
@dataclass
class Station:
    coordinates : Point
    id: int
    name : str