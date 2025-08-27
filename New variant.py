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

@dataclass
class Station:
    coordinates : Point
    id: int
    name : str

@dataclass
class Picks:
    id: int
    name: str
    p_time: float
    s_time: float

@dataclass
class Calculation:
    vp: float
    vs: float
    #Вычисление расстояния по приходу волн (будем далее использовать ... часто?)
    def distant_calculation(self, picks : Picks):
        p_time = picks.p_time
        s_time = picks.s_time
        distant = (s_time - p_time)/(self.vp - self.vs)*self.vs*self.vp
        return distant
    def Direct_task(self, station : Station, event : Event):
        distance = geodist(station.coordinates, event.coordinates)
        p_time = distance.km/self.vp
        s_time = distance.km/self.vs
        return Picks(id = station.id, name = station.name, p_time = p_time, s_time = s_time)


    def Inverse_task(self, stations : [Station] , picks : [Picks]):
        data = {
            'station' : [],
            'lon' : [],
            'lat' : [],
            'P_time':[],
            'S_time':[]
        }
        for i in range(len(stations)):
            data['station'].append(stations[i].id)
            data['lon'].append(stations[i].coordinates.longitude)
            data['lat'].append(stations[i].coordinates.latitude)
            data['P_time'].append(picks[i].p_time)
            data['S_time'].append(picks[i].s_time)
        df = pd.DataFrame(data)
        print(df)
        #теперь надо отсортировать по времени прихода волн
        df = df.sort_values(by='P_time', ascending=True)
        print(df)
        df = df.reset_index(drop=True)
        print(df)
        #теперь нам нужно учесть вес каждой станции
        length = len(df)
        cloest_station = df.iloc[0]
        cls_time = cloest_station['P_time']
        #Координаты этой станции имеют вес 1, остальные будут иметь меньший вес.
        mean_lon = 0
        mean_lat = 0
        for i in range(len(df)):
            mean_lon += df.iloc[i]['lon']*(cls_time/df.iloc[i]['P_time'])
            mean_lat += df.iloc[i]['lat'] * (cls_time / df.iloc[i]['P_time'])
        mean_lat = mean_lat/len(df)
        mean_lon = mean_lon / len(df)
        initial_guess = (mean_lon, mean_lat)
        print(initial_guess)
        #Ура у нас есть начальное предположение для метода нименьших квадратов
        #теперь можно приступать к МНК
        def mnk_function(event, stations, distances):
            mnk_d = abs(geodist(event, stations) - distances)
            return mnk_d













#test
test_event = Event(coordinates = Point(52.34, 42.43, 0), time = 0)
test_station = Station(coordinates= Point(70.38, 32.40, 0), id = 1, name = 'test')
test_calculation = Calculation(vp = 3, vs = 2)
print(test_calculation.Direct_task(test_station, test_event))

test_station2 = Station(coordinates= Point(53.38, 14.40, 0), id = 2, name = 'test2')
test_station3 = Station(coordinates= Point(23.38, 11.40, 0), id = 3, name = 'test3')
test_stations = [test_station, test_station2, test_station3]
test_peaks = [test_calculation.Direct_task(x, test_event) for x in test_stations]
test_calculation.Inverse_task(test_stations, test_peaks)






