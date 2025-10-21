#Эта программа будет переводить файлы из формата геопэкэдж в читаемый питоном класс
from dataclasses import dataclass
import shapely as shp
import geopandas as gp
import gpxpy
import pandas as pd
from src import Station
from geopy.location import Point
import json
from pathlib import Path
from src import Picks


@dataclass
class Interpreter:
    def s_exls(self, path):
        df = pd.read_excel(path, usecols= "A:D")
        stations = []
        for i in range(len(df)):
            row = df.iloc[i]
            stations.append(Station(name=row['Name'],id= i, coordinates=Point(latitude=row['Latitude'], longitude=row['Longitude'],altitude=row['Altitude'])))
        return stations

    def s_gpx(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            gpx = gpxpy.parse(f)
        station_points = []
        for waypoint in gpx.waypoints:
            station_points.append(Station(coordinates= Point(latitude=waypoint.latitude,
                                                             longitude=waypoint.longitude,
                                                             altitude=float(
                                                                 waypoint.elevation) if waypoint.elevation is not None else 0.0
                                                             ),
                                          name= waypoint.name, id= 0))
        return station_points

    def p_json(self, path):
        picks = []
        folder = Path(path)
        for json_file in folder.glob('*.json'):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for station in data:
                    picks.append(Picks(id = 0, name= station, p_time= data[station]['P']
                                       ,s_time= data[station]['S']))
        return picks









