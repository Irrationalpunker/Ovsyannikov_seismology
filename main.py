from src.Calculations import Calculations
from src.Event import Event
from src.Station import Station
from src.Picks import Picks
from src.geopackager import Unpack

#Проверка, с примерами
C1 = Calculations(vp= 4000, vs= 3000)
SS0 = Station(id= 0, coordinates= [0,0,100])
SS1 = Station(id= 1, coordinates= [14,12,99])
SS2 = Station(id= 2, coordinates= [34,23,96])
SS3 = Station(id= 3, coordinates= [56,69,92])
SS4 = Station(id= 4, coordinates= [70,18,87])
SS5 = Station(id= 5, coordinates= [89,5,95])

stations1 = Unpack("C:/Users/Irrat/Desktop/pypoints.gpkg")
#stations1 = [SS0, SS1, SS2, SS3, SS4, SS5]
Eq1 = Event(coordinates = [411328, 8029540, 5500], t0= 0)
Pikcs1 = C1.direct_task(stations1, Eq1)
print("Current piks = ",*Pikcs1)

Eq10 = C1.inverse_task(stations1,Pikcs1)
print(Eq10)