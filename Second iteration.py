from dataclasses import dataclass
from math import sqrt

import numpy as np
from scipy.optimize import minimize


@dataclass
class Picks:
    id: int
    P_time: float
    S_time: float


@dataclass
class Station:
    id: int
    scord : [float, float, float]


@dataclass
class Event:
    ecord : [float, float, float]
    t0: float


@dataclass
class Calculations:
    vp : float
    vs : float

    def dist_calculation(self, pick : Picks):
        tp = pick.P_time
        ts = pick.S_time
        d = (ts - tp)/(self.vp - self.vs)*self.vs*self.vp
        return d

    def inverse_task(self, stations : [Station], piks : [Picks]):

        #Searching for event_coordinates
        stc = [] #Stations_coordinates
        std = [] #Stations_distances
        ppt = [] #P_picks_time
        spt = [] #S_picks_time
        for j in range(len(piks)):
            ppt.append(piks[j].P_time)
            spt.append(piks[j].S_time)
        ppt = np.array(ppt)
        spt = np.array(spt)
        #Получили вектора для времени пиков, можем использовать при нахождении t0
        for i in range(len(stations)):
            stc.append(stations[i].scord)
            std.append(self.dist_calculation(piks[i]))
        stc = np.array(stc)
        std = np.array(std)
        #Приготовили два ветора, готовые для поиска наименьших квадратов
        def main_function(event_coords, stations_coords, ready_distance):
            to_minimaize = np.sqrt(np.sum((event_coords-stations_coords)**2, axis=1)) - ready_distance
            return np.sum(to_minimaize**2)

        initial_guess = [0,0,0] #Тут надо наверное что-то получше придумать

        result = minimize(main_function, initial_guess, args=(stc, std))
        d = np.sqrt(np.sum((np.array(result.x) - stc)**2, axis=1))
        dp = d/self.vp
        ds = d/self.vs
        t0p = ppt - dp
        t0s = spt - ds
        t0 = np.median(np.concatenate((t0p, t0s)))
        t0 = np.round(t0, 6)



        if result.success:
            return Event(ecord= np.round(result.x, 4), t0= float(t0) )

        else:
            print("Ошибка/Error")



    def direct_task(self, stations : [Station], event : Event):
        picks = []
        for i in range(len(stations)):
            dist = 0
            for j in range(3):
                dist += (stations[i].scord[j] - event.ecord[j])**2
            dist = sqrt(dist)
            tp = event.t0 + dist / self.vp
            ts = event.t0 + dist / self.vs
            pick = Picks(id= stations[i].id, P_time= tp, S_time= ts)
            picks.append(pick)
        return picks






#Проверка, с примерами
C1 = Calculations(vp= 2, vs= 1)
SS0 = Station(id= 0, scord= [0,0,100])
SS1 = Station(id= 1, scord= [14,12,99])
SS2 = Station(id= 2, scord= [34,23,96])
SS3 = Station(id= 3, scord= [56,69,92])
SS4 = Station(id= 4, scord= [70,18,87])
SS5 = Station(id= 5, scord= [89,5,95])


stations1 = [SS0, SS1, SS2, SS3, SS4, SS5]
Eq1 = Event(ecord= [44.33, 0.213, 54.47], t0= 0)
Pikcs1 = C1.direct_task(stations1, Eq1)
print("Current piks = ",*Pikcs1)

Eq10 = C1.inverse_task(stations1,Pikcs1)
print(Eq10)



