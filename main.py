from src.Calculations import Calculation
from geopy.location import Point
from src.Station import Station
from src.Event import Event
from src.geopackager import Interpreter
#
# test_event = Event(coordinates=Point(51.34, 42.43, 0), time=0)
# test_station = Station(coordinates=Point(70.38, 32.40, 0), id=1, name='test')
# test_calculation = Calculation(vp=3, vs=2)
# print(test_calculation.Direct_task(test_station, test_event))
# test_station2 = Station(coordinates=Point(53.38, 14.40, 0), id=2, name='test2')
# test_station3 = Station(coordinates=Point(23.38, 11.40, 0), id=3, name='test3')
# test_stations = [test_station, test_station2, test_station3]
# test_peaks = [test_calculation.Direct_task(x, test_event) for x in test_stations]
# print(test_calculation.Inverse_task(test_stations, test_peaks))

I1 = Interpreter()
Stations = I1.s_gpx(r"C:\Users\Irrat\Desktop\2024-07.BBB-BSP.gpx")
print(Stations)


#
# #Проверка, с примерами
# C1 = Calculations(vp= 4000, vs= 3000)
# SS0 = Station(id= 0, coordinates= [0,0,100])
# SS1 = Station(id= 1, coordinates= [14,12,99])
# SS2 = Station(id= 2, coordinates= [34,23,96])
# SS3 = Station(id= 3, coordinates= [56,69,92])
# SS4 = Station(id= 4, coordinates= [70,18,87])
# SS5 = Station(id= 5, coordinates= [89,5,95])
#
# stations1 = Unpack("C:/Users/Irrat/Desktop/pypoints.gpkg")
# #stations1 = [SS0, SS1, SS2, SS3, SS4, SS5]
# Eq1 = Event(coordinates = [411328, 8029540, 5500], t0= 0)
# Pikcs1 = C1.direct_task(stations1, Eq1)
# print("Current piks = ",*Pikcs1)
#
# Eq10 = C1.inverse_task(stations1,Pikcs1)
# print(Eq10)