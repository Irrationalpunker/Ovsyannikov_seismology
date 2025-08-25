from dataclasses import dataclass
from math import sqrt
import numpy as np
from scipy.optimize import minimize
from .Picks import Picks
from .Event import Event
from .Station import Station
@dataclass
class Calculations:
    vp : float
    vs : float

    def dist_calculation(self, pick : Picks):
        tp = pick.P_time
        ts = pick.S_time
        d = (ts - tp)/(self.vp - self.vs)*self.vs*self.vp
        return d

    def inverse_task(self, stations : [Station], picks : [Picks]):

        #Searching for event_coordinates
        stc = [] #Stations_coordinates
        std = [] #Stations_distances
        ppt = [] #P_picks_time
        spt = [] #S_picks_time
        for j in range(len(picks)):
            ppt.append(picks[j].P_time)
            spt.append(picks[j].S_time)
        ppt = np.array(ppt)
        spt = np.array(spt)
        #Получили вектора для времени пиков, можем использовать при нахождении t0
        for i in range(len(stations)):
            stc.append(stations[i].coordinates)
            std.append(self.dist_calculation(picks[i]))
        stc = np.array(stc)
        std = np.array(std)
        #Приготовили два вектора, готовые для поиска наименьших квадратов
        def main_function(event_coords, stations_coords, ready_distance):
            to_minimaize = np.sqrt(np.sum((event_coords-stations_coords)**2, axis=1)) - ready_distance
            return np.sum(to_minimaize**2)

        initial_guess = [411320,8029540,6000] #Тут надо наверное что-то получше придумать

        result = minimize(main_function, initial_guess, args=(stc, std))
        d = np.sqrt(np.sum((np.array(result.x) - stc)**2, axis=1))
        dp = d/self.vp
        ds = d/self.vs
        t0p = ppt - dp
        t0s = spt - ds
        t0 = np.median(np.concatenate((t0p, t0s)))
        t0 = np.round(t0, 6)



        if result.success:
            return Event(coordinates= np.round(result.x, 4), t0= float(t0) )

        else:
            print("Ошибка/Error")
            print(result)



    def direct_task(self, stations : [Station], event : Event):
        picks = []
        for i in range(len(stations)):
            dist = 0
            for j in range(3):
                dist += (stations[i].coordinates[j] - event.coordinates[j])**2
            dist = sqrt(dist)
            tp = event.t0 + dist / self.vp
            ts = event.t0 + dist / self.vs
            pick = Picks(id= stations[i].id, P_time= tp, S_time= ts)
            picks.append(pick)
        return picks
