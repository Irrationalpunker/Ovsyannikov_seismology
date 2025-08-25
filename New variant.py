from dataclasses import dataclass
from geopy.distance import distance as geodist
from geopy.location import Point
import numpy
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
        stations_points = []    # лист для координат станций
        picks_p_times = []      # лист для первичных пиков
        picks_s_times = []      # лист для вторичных пиков
        distnces = []           # лист для дистанций по пикам
        for i in range(len(stations)): #Важно, что станций должно быть столько же сколько и пиков, и в массивах они должны быть в одном порядке
            stations_points.append(stations[i].coordiantes)
            picks_p_times.append(picks.p_time)
            picks_s_times.append(picks.s_time)
            distnces.append(self.distant_calculation(picks[i]))
        stations_points = numpy.array(stations_points)  # массив для координат станций
        picks_p_times = numpy.array(picks_p_times)      # массив для первичных пиков
        picks_s_times = numpy.array(picks_s_times)      # массив для вторичных пиков
        distnces = numpy.array(distnces)                # массив для дистанций по пикам

        initial_guess = 












#test
test_event = Event(coordinates = Point(52.34, 42.43, 0), time = 0)
test_station = Station(coordinates= Point(52.38, 42.40, 0), id = 1, name = 'test')
test_calculation = Calculation(vp = 3, vs = 2)
print(test_calculation.Direct_task(test_station, test_event))






