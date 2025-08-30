from dataclasses import dataclass
from geopy.location import Point

@dataclass
class Event:
    coordinates : Point
    time : float