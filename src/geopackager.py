#Эта программа будет переводить файлы из формата геопэкэдж в читаемый питоном класс
import shapely as shp
import geopandas as gp
import pandas as pd
from src import Station

def Unpack(stations_directory, picks_directory = None):
    import geopandas as gp
    import pandas as pd
    points = gp.read_file(stations_directory)
    geo = points['geometry']
    stations = []
    for i in range(len(geo)):
        stations.append(Station(id=i, coordinates=[geo[i].x, geo[i].y, 6000]))
    return stations



