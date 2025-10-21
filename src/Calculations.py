from dataclasses import dataclass
from geopy.distance import distance as geodist
from geopy.location import Point
import pandas as pd
from scipy.optimize import minimize
from src.Station import Station
from src.Picks import Picks
from src.Event import Event
from pyproj import Transformer
import numpy as np


@dataclass
class Calculation:
    vp: float
    vs: float
    transformer = Transformer.from_crs("EPSG:4326",
                                       "EPSG:4978",
                                       always_xy=True)
    #Вычисление расстояния по приходу волн (будем далее использовать ... часто?)
    def distant_calculation(self, picks : Picks):
        p_time = picks.p_time
        s_time = picks.s_time
        distant = (s_time - p_time)/(self.vp - self.vs)*self.vs*self.vp
        return distant

    def Direct_task(self, station : Station, event : Event): #надо тоже переписать
        distance = geodist(station.coordinates, event.coordinates)
        p_time = distance.km/self.vp
        s_time = distance.km/self.vs
        return Picks(id = station.id, name = station.name, p_time = p_time, s_time = s_time)


    def Inverse_task(self, stations : [Station] , picks : [Picks]):
        station_by_name = {s.name: s for s in stations}
        pick_by_name = {p.name: p for p in picks}
        common_names = set(station_by_name.keys()) & set(pick_by_name.keys())

        data = {
            'station' : [],
            'name' :[],
            'lat' : [],
            'lon' : [],
            'alt' : [],
            'P_time':[],
            'S_time':[]
        }
        for name in common_names:
            station = station_by_name[name]
            pick = pick_by_name[name]

            data['station'].append(station.id)
            data['lat'].append(station.coordinates.latitude)
            data['lon'].append(station.coordinates.longitude)
            data['P_time'].append(pick.p_time)
            data['S_time'].append(pick.s_time)
            data['name'].append(station.name)
            data['alt'].append(station.coordinates.altitude)
        df = pd.DataFrame(data)
        print(df)
        df['x'] , df['y'], df['z'] = self.transformer.transform(df['lon'],df['lat'],df['alt'])
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
        mean_alt = 0
        for i in range(len(df)):
            mean_lon += df.iloc[i]['lon']*(cls_time/df.iloc[i]['P_time'])
            mean_lat += df.iloc[i]['lat']*(cls_time / df.iloc[i]['P_time'])
            mean_alt += df.iloc[i]['alt']*(cls_time / df.iloc[i]['P_time'])
        mean_lat = mean_lat/len(df)
        mean_lon = mean_lon/len(df)
        mean_alt = mean_alt/len(df)
        initial_guess = self.transformer.transform(mean_lon, mean_lat, mean_alt)
        print('Начальное предположение координат эпицентра',*initial_guess)
        #Ура у нас есть начальное предположение для метода наименьших квадратов
        #теперь можно приступать к МНК
        #Но сначала добавим в df столбец тру расстояний от станции до эпицентра
        df['dist'] = self.distant_calculation(picks= Picks(p_time=df['P_time'],s_time=df['S_time'], id= df['station'],name= None))
        print(df)

        def mnk_function(event, df):
            total_error : float = 0
            x, y, z = event
            for i in df.index:
                xi = df.at[i, 'x']
                yi = df.at[i, 'y']
                zi = df.at[i, 'z']
                dist_observed = df.at[i, 'dist']

                dist_computed = np.sqrt((x - xi) ** 2 + (y - yi) ** 2 + (z - zi) ** 2)

                residual = dist_computed - dist_observed

                total_error += residual ** 2

            return total_error

        result = minimize(mnk_function, initial_guess,args=(df), method='Nelder-Mead', options={'disp': True})

        if result.success:
            x, y, z = result.x
            print(f"Эпицентр найден")
            return [x, y, z]
        else:
            print("Эпицентр не найден", result.message)