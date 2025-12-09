import pickle
from pathlib import Path
from climateTrends.station import Station
import math

def load_stations(p: Path):
    '''load previously pickled climate stations'''
    with open(p, 'rb') as f:
        data =  pickle.load(f)
        return data

def find_nearest(stations, lat, lon) -> Station:
    '''find closest climate station based on Euclidean distance'''
    min_distance = float('inf')
    nearest_station = None
    for station in stations:
        station_lat, station_lon = station.coordinates
        distance = math.sqrt((lat - station_lat)**2 + (lon - station_lon)**2)
        if distance < min_distance:
            min_distance = distance
            nearest_station = station
    return nearest_station

