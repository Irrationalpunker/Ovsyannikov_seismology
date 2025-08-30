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
            'lat' : [],
            'lon' : [],
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
        initial_guess = (mean_lat, mean_lon)
        print('Начальное предположение координат эпицентра',*initial_guess)
        #Ура у нас есть начальное предположение для метода наименьших квадратов
        #теперь можно приступать к МНК
        #Но сначала добавим в df столбец тру расстояний от станции до эпицентра
        df['dist'] = self.distant_calculation(picks= Picks(p_time=df['P_time'],s_time=df['S_time'], id= df['station'],name= None))
        print(df)

        def mnk_function(event, dataframe):#координаты ивента в формате (лат, лон)
            full_error : float = 0
            for i in dataframe.index:
                error: float = 0
                error += geodist(event, (dataframe.at[i, 'lat'], dataframe.at[i, 'lon'])).km - dataframe.at[i,'dist']
                full_error += error **2
            return full_error

        result = minimize(mnk_function, initial_guess,args=(df), method='BFGS', options={'disp': True})

        if result.success:
            event_lat, event_lon = result.x
            print(f"Эпицентр найден")
            return Event(coordinates=Point(latitude=event_lat, longitude=event_lon, altitude=0),time= None)
        else:
            print("Эпицентр не найден", result.message)



def package(stations_directory = None, picks_directory= None ):
    if stations_directory != None:
        stations_points = gpd.read_file(stations_directory)
        stations_geometry = stations_points['geometry']
        stations = []
        for i in range(len(stations_geometry)):
            stations.append(Station(coordinates= Point(latitude=stations_geometry[i].lat,longitude=stations_geometry[i].lon,altitude=0)))
    if picks_directory != None:
        picks= None
    return( stations , picks )#Надо понимать в каком формате будут поставляться пики, чтобы их ывгружать













#test
DEBUGE1 = False
#test
if DEBUGE1 == True:
    test_event = Event(coordinates=Point(51.34, 42.43, 0), time=0)
    test_station = Station(coordinates=Point(70.38, 32.40, 0), id=1, name='test')
    test_calculation = Calculation(vp=3, vs=2)
    print(test_calculation.Direct_task(test_station, test_event))
    test_station2 = Station(coordinates=Point(53.38, 14.40, 0), id=2, name='test2')
    test_station3 = Station(coordinates=Point(23.38, 11.40, 0), id=3, name='test3')
    test_stations = [test_station, test_station2, test_station3]
    test_peaks = [test_calculation.Direct_task(x, test_event) for x in test_stations]
    print(test_calculation.Inverse_task(test_stations, test_peaks))



#test
DEBUGE2 = False
#test
if DEBUGE2 == True:
    test_event = Event(coordinates=Point(51.34, 42.43, 0), time=0)
    test_stations = (package('"C:/Users/Irrat/Desktop/pypoints.gpkg"'))
    test_calculation = Calculation(vp= 6, vs= 5)
    test_stations = test_calculation.Direct_task(test_stations, test_event)




