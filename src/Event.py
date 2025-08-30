from dataclasses import dataclass
from geopy.distance import distance as geodist
from geopy.location import Point
import numpy
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point as shpp
from scipy.optimize import minimize
@dataclass
class Event:
    coordinates : Point
    time : float